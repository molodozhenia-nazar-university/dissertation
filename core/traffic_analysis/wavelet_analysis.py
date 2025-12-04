import warnings

warnings.filterwarnings("ignore")

import numpy
import pywt

from scapy.all import (
    rdpcap,
    TCP,
    UDP,
    ICMP,
    DNS,
    ARP,
    BOOTP,
    DHCP,
    IP,
    IPv6,
)

from core.traffic_analysis.traffic_analysis_information import (
    set_packets,
    set_packets_information,
    build_packets_information,
)


# ==========================
#  ДОПОМІЖНІ ФУНКЦІЇ
# ==========================


def is_private_ipv4(ip: str) -> bool:
    """Простий чек, чи адреса в приватних діапазонах."""
    if not ip:
        return False
    try:
        parts = [int(p) for p in ip.split(".")]
        if len(parts) != 4:
            return False
        if parts[0] == 10:
            return True
        if parts[0] == 172 and 16 <= parts[1] <= 31:
            return True
        if parts[0] == 192 and parts[1] == 168:
            return True
    except Exception:
        return False
    return False


def extract_traffic_features(packets):
    """
    Витягуємо базові характеристики:
    - timestamps: час кожного пакета
    - sizes: розмір пакета
    - protocols: протокол верхнього рівня (TCP/UDP/ICMP/DNS/OTHER)
    """

    timestamps = []
    sizes = []
    protocols = []

    for packet in packets:
        if hasattr(packet, "time"):
            timestamps.append(float(packet.time))
        if hasattr(packet, "len"):
            sizes.append(int(packet.len))
        else:
            # запасний варіант
            try:
                sizes.append(len(bytes(packet)))
            except Exception:
                sizes.append(0)

        proto = "OTHER"
        if packet.haslayer(TCP):
            proto = "TCP"
        elif packet.haslayer(UDP):
            proto = "UDP"
        elif packet.haslayer(ICMP):
            proto = "ICMP"
        elif packet.haslayer(DNS):
            proto = "DNS"
        protocols.append(proto)

    return timestamps, sizes, protocols


def create_time_series(timestamps, sizes, interval_sec=1):
    """
    Створюємо часові ряди:
    - traffic_volume: сумарний розмір пакетів за інтервал
    - packet_count: кількість пакетів за інтервал
    """

    if not timestamps:
        return numpy.array([]), numpy.array([])

    start_time = min(timestamps)
    end_time = max(timestamps)

    if end_time <= start_time:
        return numpy.array([]), numpy.array([])

    time_bins = numpy.arange(start_time, end_time + interval_sec, interval_sec)

    if len(time_bins) < 2:
        return numpy.array([]), numpy.array([])

    traffic_volume = numpy.zeros(len(time_bins) - 1, dtype=float)
    packet_count = numpy.zeros(len(time_bins) - 1, dtype=float)

    for ts, size in zip(timestamps, sizes):
        bin_idx = int((ts - start_time) // interval_sec)
        if 0 <= bin_idx < len(traffic_volume):
            traffic_volume[bin_idx] += size
            packet_count[bin_idx] += 1

    return traffic_volume, packet_count


def detect_anomalies_wavelet(signal, wavelet="db4", level=6, threshold_std=3.0):
    """
    Виявлення аномалій за допомогою вейвлет-аналізу.
    Повертає:
        anomalies: словник з high_freq_anomalies, low_freq_anomalies тощо
        coeffs: усі коефіцієнти вейвлет-розкладання
    """
    signal = numpy.asarray(signal, dtype=float)

    anomalies = {
        "high_freq_anomalies": [],
        "low_freq_anomalies": [],
        "trend_breaks": [],
        "spikes": [],
    }

    if signal.size == 0:
        return anomalies, []

    # Якщо сигнал закороткий, коригуємо рівень
    max_level = int(numpy.log2(signal.size)) if signal.size > 0 else 1
    if max_level < 1:
        return anomalies, []
    if level > max_level:
        level = max_level

    try:
        coeffs = pywt.wavedec(signal, wavelet, level=level)

        # Деталізуючі коефіцієнти (високочастотні)
        detail_coeffs = coeffs[1:]

        for i, detail in enumerate(detail_coeffs):
            if detail.size == 0:
                continue

            std_level = numpy.std(detail)
            mean_level = numpy.mean(detail)

            if std_level == 0:
                continue

            # Викиди
            outliers = numpy.where(
                numpy.abs(detail - mean_level) > threshold_std * std_level
            )[0]

            for outlier_idx in outliers:
                time_position = outlier_idx * (2 ** (i + 1))
                magnitude = float(detail[outlier_idx])

                anomalies["high_freq_anomalies"].append(
                    {
                        "time_position": int(time_position),
                        "magnitude": magnitude,
                        "level": i + 1,
                        "type": "HIGH_FREQ",
                    }
                )

        # Апроксимуючі коефіцієнти (низькочастотні, тренд)
        approx_coeffs = coeffs[0]
        if approx_coeffs.size > 10:
            std_approx = numpy.std(approx_coeffs)
            mean_approx = numpy.mean(approx_coeffs)

            if std_approx > 0:
                trend_changes = numpy.where(
                    numpy.abs(approx_coeffs - mean_approx) > 2 * std_approx
                )[0]

                for change_idx in trend_changes:
                    anomalies["low_freq_anomalies"].append(
                        {
                            "time_position": int(change_idx * (2**level)),
                            "magnitude": float(approx_coeffs[change_idx]),
                            "type": "TREND_CHANGE",
                        }
                    )

        return anomalies, coeffs

    except Exception as e:
        print(f"Помилка вейвлет-аналізу: {e}")
        return anomalies, []


def analyze_protocol_anomalies(protocols, timestamps):
    """
    Аналіз протокольних аномалій:
    - протоколи, у яких багато "спалахів" активності.
    """

    protocol_counts = {}
    protocol_timelines = {}

    for proto, ts in zip(protocols, timestamps):
        protocol_counts[proto] = protocol_counts.get(proto, 0) + 1
        protocol_timelines.setdefault(proto, []).append(ts)

    anomalies = []

    for proto, times in protocol_timelines.items():
        if len(times) <= 10:
            continue

        times_sorted = sorted(times)
        time_diff = numpy.diff(times_sorted)

        if time_diff.size == 0:
            continue

        avg_interval = float(numpy.mean(time_diff))
        std_interval = float(numpy.std(time_diff))

        if std_interval == 0:
            continue

        bursts = numpy.where(time_diff < avg_interval - 2 * std_interval)[0]
        if bursts.size > 0.3 * time_diff.size:
            anomalies.append(
                {
                    "type": "PROTOCOL_BURST",
                    "protocol": proto,
                    "burst_count": int(bursts.size),
                    "severity": (
                        "HIGH" if bursts.size > 0.5 * time_diff.size else "MEDIUM"
                    ),
                }
            )

    return anomalies, protocol_counts


def analyze_dns(packets):
    """
    Аналіз DNS:
    - загальна кількість запитів
    - кількість відповідей з помилками (NXDOMAIN, SERVFAIL, ...)
    - кількість запитів без відповіді (не ідеально, але дає індикатор)
    """

    total_queries = 0
    error_responses = 0

    queries = {}  # ключ: (id, qname) -> кількість
    answers_seen = set()  # ключ: (id, qname)

    problem_domains = {}

    for pkt in packets:
        if not pkt.haslayer(DNS):
            continue

        dns = pkt[DNS]

        qname = None
        if dns.qdcount > 0 and dns.qd is not None:
            try:
                qname = dns.qd.qname.decode(errors="ignore")
            except Exception:
                qname = str(dns.qd.qname)
        else:
            qname = "unknown"

        key = (dns.id, qname)

        # Запит
        if dns.qr == 0:
            total_queries += 1
            queries[key] = queries.get(key, 0) + 1

        # Відповідь
        else:
            answers_seen.add(key)
            if dns.rcode != 0:
                error_responses += 1
                problem_domains[qname] = problem_domains.get(qname, 0) + 1

    # Запити без відповіді
    unanswered = 0
    for key, count in queries.items():
        if key not in answers_seen:
            unanswered += count

    failure_rate = (
        (error_responses + unanswered) / total_queries if total_queries > 0 else 0.0
    )

    return {
        "total_queries": int(total_queries),
        "error_responses": int(error_responses),
        "unanswered_queries": int(unanswered),
        "failure_rate": float(failure_rate),
        "problem_domains": problem_domains,
    }


def analyze_ip_addressing(packets):
    """
    Аналіз DHCP + ARP для виявлення проблем адресації:
    - DHCP DISCOVER / OFFER / REQUEST / ACK
    - ARP-конфлікти IP (одна IP -> кілька MAC)
    """

    dhcp_discover = dhcp_offer = dhcp_request = dhcp_ack = 0
    arp_ip_usage = {}

    for pkt in packets:
        # DHCP
        if pkt.haslayer(DHCP) and pkt.haslayer(BOOTP):
            dhcp = pkt[DHCP]
            opts = dhcp.options
            msg_type = None
            for opt in opts:
                if isinstance(opt, tuple) and opt[0] == "message-type":
                    msg_type = opt[1]
                    break

            if msg_type == 1:
                dhcp_discover += 1
            elif msg_type == 2:
                dhcp_offer += 1
            elif msg_type == 3:
                dhcp_request += 1
            elif msg_type == 5:
                dhcp_ack += 1

        # ARP
        if pkt.haslayer(ARP):
            arp = pkt[ARP]
            if arp.psrc:
                arp_ip_usage.setdefault(arp.psrc, set()).add(arp.hwsrc)

    ip_conflicts = {
        ip: list(macs) for ip, macs in arp_ip_usage.items() if len(macs) > 1
    }

    return {
        "dhcp_discover": int(dhcp_discover),
        "dhcp_offer": int(dhcp_offer),
        "dhcp_request": int(dhcp_request),
        "dhcp_ack": int(dhcp_ack),
        "ip_conflicts": ip_conflicts,
    }


def analyze_security(packets):
    """
    Аналіз безпеки:
    - можливі порт-скани (багато SYN на різні порти без нормального встановлення)
    - високий відсоток SYN без ACK
    """

    # Для кожного джерела — на які порти він шле SYN
    syn_by_src = {}
    syn_total = 0
    syn_no_ack = 0

    # Відстеження, де був SYN+ACK
    synack_seen = set()  # (src_ip, dst_ip, dport)

    for pkt in packets:
        if not pkt.haslayer(TCP):
            continue

        tcp = pkt[TCP]

        src_ip = None
        dst_ip = None
        if pkt.haslayer(IP):
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
        elif pkt.haslayer(IPv6):
            src_ip = pkt[IPv6].src
            dst_ip = pkt[IPv6].dst

        if src_ip is None or dst_ip is None:
            continue

        flags = int(tcp.flags)

        # SYN
        if flags & 0x02 and not (flags & 0x10):  # SYN без ACK
            syn_total += 1
            syn_by_src.setdefault(src_ip, set()).add(tcp.dport)

        # SYN+ACK
        if (flags & 0x02) and (flags & 0x10):
            synack_seen.add((dst_ip, src_ip, tcp.sport))  # відповідь сервер -> клієнт

    # Оцінюємо SYN без SYN+ACK
    for pkt in packets:
        if not pkt.haslayer(TCP) or not pkt.haslayer(IP):
            continue

        tcp = pkt[TCP]
        ip = pkt[IP]
        flags = int(tcp.flags)

        if flags & 0x02 and not (flags & 0x10):  # SYN
            key = (ip.src, ip.dst, tcp.dport)
            if key not in synack_seen:
                syn_no_ack += 1

    syn_no_ack_ratio = syn_no_ack / syn_total if syn_total > 0 else 0.0

    # Пошук джерел з багатьма різними портами (можливий скан)
    port_scan_sources = []
    for src, ports in syn_by_src.items():
        if len(ports) >= 20:  # поріг для "скану"
            port_scan_sources.append(
                {
                    "src_ip": src,
                    "unique_ports": len(ports),
                    "type": "POSSIBLE_PORT_SCAN",
                }
            )

    return {
        "syn_total": int(syn_total),
        "syn_no_ack": int(syn_no_ack),
        "syn_no_ack_ratio": float(syn_no_ack_ratio),
        "port_scan_sources": port_scan_sources,
    }


def analyze_external_connectivity(packets):
    """
    Аналіз зовнішніх з'єднань:
    - багато спроб з'єднання до зовнішніх IP, що не завершуються успіхом
    """

    external_syn = 0
    external_failed = 0

    # Відстеження, де з'єднання було успішним (SYN -> SYN+ACK -> ACK)
    successful_flows = set()  # (src_ip, dst_ip, dport)

    flows_syn = set()

    for pkt in packets:
        if not pkt.haslayer(TCP):
            continue

        tcp = pkt[TCP]
        if not pkt.haslayer(IP):
            continue

        ip = pkt[IP]

        src_ip = ip.src
        dst_ip = ip.dst
        dport = tcp.dport

        # Вважаємо "зовнішньою" не-приватну адресу
        if is_private_ipv4(dst_ip):
            continue

        flags = int(tcp.flags)
        flow_key = (src_ip, dst_ip, dport)

        # SYN від локального → зовнішнього
        if (flags & 0x02) and not (flags & 0x10):
            external_syn += 1
            flows_syn.add(flow_key)

        # SYN+ACK у відповідь
        if (flags & 0x02) and (flags & 0x10):
            # dst_ip тут — клієнт, src_ip — сервер
            success_key = (dst_ip, src_ip, tcp.sport)
            successful_flows.add(success_key)

    # SYN, які не мають успішного продовження
    for flow_key in flows_syn:
        if flow_key not in successful_flows:
            external_failed += 1

    failure_ratio = external_failed / external_syn if external_syn > 0 else 0.0

    return {
        "external_syn": int(external_syn),
        "external_failed": int(external_failed),
        "external_failure_ratio": float(failure_ratio),
    }


def classify_problem(
    detected_anomalies,
    dns_metrics,
    ip_metrics,
    security_metrics,
    external_metrics,
    protocol_stats,
    traffic_volume,
    packet_count,
):
    """
    Класифікація проблем у категорії:
        Q_DNS, Q_IP_ADDRESSING, Q_PERFORMANCE, Q_SECURITY, Q_EXTERNAL, NONE
    """

    issues = []
    severity_rank = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}

    total_anomalies = (
        detected_anomalies.get("volume_anomalies", 0)
        + detected_anomalies.get("packet_anomalies", 0)
        + detected_anomalies.get("protocol_anomalies", 0)
    )

    # ---------- Q_DNS ----------
    if dns_metrics["total_queries"] > 20:
        if dns_metrics["failure_rate"] > 0.7:
            issues.append(
                {
                    "code": "DNS_RESOLUTION_FAILURE",
                    "category": "Q_DNS",
                    "confidence": min(1.0, 0.5 + dns_metrics["failure_rate"]),
                    "severity": "HIGH",
                    "user_message": (
                        "Більшість DNS-запитів завершується помилкою або без відповіді. "
                        "Ймовірна проблема з DNS-серверами провайдера або їх налаштуванням."
                    ),
                    "evidence": dns_metrics,
                }
            )
        elif dns_metrics["failure_rate"] > 0.3:
            issues.append(
                {
                    "code": "DNS_INSTABILITY",
                    "category": "Q_DNS",
                    "confidence": 0.6,
                    "severity": "MEDIUM",
                    "user_message": (
                        "Частина DNS-запитів завершується помилкою або без відповіді. "
                        "Можлива нестабільність DNS-сервера."
                    ),
                    "evidence": dns_metrics,
                }
            )

    # ---------- Q_IP_ADDRESSING ----------
    if ip_metrics["dhcp_discover"] > 0 and ip_metrics["dhcp_ack"] == 0:
        issues.append(
            {
                "code": "DHCP_NO_ACK",
                "category": "Q_IP_ADDRESSING",
                "confidence": 0.85,
                "severity": "HIGH",
                "user_message": (
                    "Клієнт надсилає DHCP-запити, але не отримує підтвердження (ACK). "
                    "Можливо, відключений DHCP-сервер на роутері або вичерпано IP-адреси."
                ),
                "evidence": ip_metrics,
            }
        )

    if ip_metrics["ip_conflicts"]:
        issues.append(
            {
                "code": "IP_CONFLICT",
                "category": "Q_IP_ADDRESSING",
                "confidence": 0.9,
                "severity": "MEDIUM",
                "user_message": (
                    "Виявлено одну або більше IP-адрес, які використовуються кількома MAC-адресами. "
                    "Можливий конфлікт IP у локальній мережі."
                ),
                "evidence": ip_metrics["ip_conflicts"],
            }
        )

    # ---------- Q_PERFORMANCE ----------
    tv = numpy.asarray(traffic_volume, dtype=float)
    if tv.size > 0:
        avg_volume = float(numpy.mean(tv))
        max_volume = float(numpy.max(tv))
        spike_ratio = (max_volume / avg_volume) if avg_volume > 0 else 0.0
    else:
        avg_volume = max_volume = spike_ratio = 0.0

    if total_anomalies > 10 or spike_ratio > 5:
        issues.append(
            {
                "code": "PERFORMANCE_DEGRADATION",
                "category": "Q_PERFORMANCE",
                "confidence": 0.7 if total_anomalies < 20 else 0.85,
                "severity": "MEDIUM" if total_anomalies < 20 else "HIGH",
                "user_message": (
                    "Виявлено значні коливання об'єму трафіку. "
                    "Можливе перевантаження каналу або нестабільна робота мережі."
                ),
                "evidence": {
                    "total_anomalies": int(total_anomalies),
                    "spike_ratio": float(spike_ratio),
                },
            }
        )

    # ---------- Q_SECURITY ----------
    if (
        security_metrics["syn_no_ack_ratio"] > 0.7
        and security_metrics["syn_total"] > 50
    ):
        issues.append(
            {
                "code": "SUSPECTED_DOS",
                "category": "Q_SECURITY",
                "confidence": 0.8,
                "severity": "HIGH",
                "user_message": (
                    "Дуже багато спроб встановлення TCP-з'єднань без відповіді. "
                    "Можлива атака або масовані підключення до недоступних ресурсів."
                ),
                "evidence": security_metrics,
            }
        )

    if security_metrics["port_scan_sources"]:
        issues.append(
            {
                "code": "POSSIBLE_PORT_SCAN",
                "category": "Q_SECURITY",
                "confidence": 0.8,
                "severity": "MEDIUM",
                "user_message": (
                    "Виявлено джерела, що здійснюють багато підключень до різних портів. "
                    "Можливе сканування портів."
                ),
                "evidence": security_metrics["port_scan_sources"],
            }
        )

    # ---------- Q_EXTERNAL ----------
    if (
        external_metrics["external_syn"] > 20
        and external_metrics["external_failure_ratio"] > 0.7
        and dns_metrics["failure_rate"] < 0.3  # DNS більш-менш ок
    ):
        issues.append(
            {
                "code": "EXTERNAL_CONNECTIVITY_PROBLEM",
                "category": "Q_EXTERNAL",
                "confidence": 0.75,
                "severity": "MEDIUM",
                "user_message": (
                    "Більшість спроб підключення до зовнішніх ресурсів неуспішні. "
                    "Ймовірно, проблема поза межами локальної мережі (на боці провайдера або віддалених серверів)."
                ),
                "evidence": external_metrics,
            }
        )

    # ---------- Підсумок ----------
    if not issues:
        return {
            "main_category": "NONE",
            "severity": "LOW",
            "confidence": 1.0,
            "subcategories": [],
        }

    def issue_sort_key(issue):
        return (severity_rank.get(issue["severity"], 0), issue["confidence"])

    issues_sorted = sorted(issues, key=issue_sort_key, reverse=True)
    main = issues_sorted[0]

    return {
        "main_category": main["category"],
        "severity": main["severity"],
        "confidence": float(main["confidence"]),
        "subcategories": issues_sorted,
    }


# ==========================
#  ОСНОВНА ФУНКЦІЯ АНАЛІЗУ
# ==========================


def wavelet_analysis(file_path, wavelet_type="db4", level=6, interval_sec=1):
    """
    Головна функція:
    - читає PCAP
    - рахує часові ряди
    - виконує вейвлет-аналіз
    - збирає DNS/DHCP/ARP/безпеку/зовнішні проблеми
    - формує results з блоком diagnosis
    """

    try:
        print(f"📖 Читання PCAP файлу: {file_path}")
        packets = rdpcap(file_path)

        if len(packets) == 0:
            return {"error": "Файл не містить пакетів"}

        print(f"📦 Обробка {len(packets)} пакетів...")

        # Зберігаємо пакети для інших вікон (як було раніше)
        set_packets(packets)
        set_packets_information(build_packets_information(packets))

        # Базові характеристики
        timestamps, sizes, protocols = extract_traffic_features(packets)

        # Часові ряди
        traffic_volume, packet_count = create_time_series(
            timestamps, sizes, interval_sec=interval_sec
        )

        if traffic_volume.size == 0:
            return {"error": "Не вдалося створити часові ряди"}

        # Нормалізація (обережно зі std == 0)
        tv_std = numpy.std(traffic_volume)
        tv_mean = numpy.mean(traffic_volume)
        if tv_std == 0:
            traffic_normalized = numpy.zeros_like(traffic_volume, dtype=float)
        else:
            traffic_normalized = (traffic_volume - tv_mean) / tv_std

        pc_std = numpy.std(packet_count)
        pc_mean = numpy.mean(packet_count)
        if pc_std == 0:
            packet_normalized = numpy.zeros_like(packet_count, dtype=float)
        else:
            packet_normalized = (packet_count - pc_mean) / pc_std

        # Вейвлет-аналіз
        print("🔍 Виконання вейвлет-аналізу Добеші ДБ4...")

        volume_anomalies, volume_coeffs = detect_anomalies_wavelet(
            traffic_normalized, wavelet_type, level
        )
        packet_anomalies, packet_coeffs = detect_anomalies_wavelet(
            packet_normalized, wavelet_type, level
        )

        # Протокольні аномалії
        protocol_anomalies, protocol_stats = analyze_protocol_anomalies(
            protocols, timestamps
        )

        # DNS
        dns_metrics = analyze_dns(packets)

        # IP-адресація (DHCP+ARP)
        ip_metrics = analyze_ip_addressing(packets)

        # Безпека (порт-скани / SYN flood)
        security_metrics = analyze_security(packets)

        # Зовнішні проблеми (провайдер/сервери)
        external_metrics = analyze_external_connectivity(packets)

        # Підсумкові лічильники
        detected_anomalies = {
            "volume_anomalies": len(volume_anomalies.get("high_freq_anomalies", [])),
            "packet_anomalies": len(packet_anomalies.get("high_freq_anomalies", [])),
            "protocol_anomalies": len(protocol_anomalies),
            "trend_changes": len(volume_anomalies.get("low_freq_anomalies", [])),
        }

        # Діагностика (категорії Q_...)
        diagnosis = classify_problem(
            detected_anomalies,
            dns_metrics,
            ip_metrics,
            security_metrics,
            external_metrics,
            protocol_stats,
            traffic_volume,
            packet_count,
        )

        # Загальна статистика
        results = {
            "summary": {
                "total_packets": len(packets),
                "analysis_duration": f"{len(traffic_volume)} інтервалів по {interval_sec} с",
                "wavelet_type": wavelet_type,
                "wavelet_level": level,
            },
            "traffic_stats": {
                "total_volume": int(sum(sizes)),
                "avg_packet_size": float(numpy.mean(sizes)) if sizes else 0.0,
                "time_range": (
                    f"{min(timestamps) if timestamps else 0:.1f} - "
                    f"{max(timestamps) if timestamps else 0:.1f} сек"
                ),
            },
            "protocol_distribution": protocol_stats,
            "detected_anomalies": detected_anomalies,
            "detailed_findings": {
                "high_frequency_spikes": volume_anomalies.get(
                    "high_freq_anomalies", []
                ),
                "traffic_trend_changes": volume_anomalies.get("low_freq_anomalies", []),
                "protocol_bursts": protocol_anomalies,
                "dns_metrics": dns_metrics,
                "ip_addressing_metrics": ip_metrics,
                "security_metrics": security_metrics,
                "external_metrics": external_metrics,
            },
            "diagnosis": diagnosis,
            "diagnosis_aux": {
                "dns": dns_metrics,
                "ip_addressing": ip_metrics,
                "security": security_metrics,
                "external": external_metrics,
            },
            "recommendations": [],
        }

        # Старий «глобальний» рівень загроз — залишаємо, але можемо доповнити
        total_anomalies = (
            detected_anomalies["volume_anomalies"]
            + detected_anomalies["packet_anomalies"]
            + detected_anomalies["protocol_anomalies"]
        )

        if total_anomalies > 20:
            results["recommendations"].append(
                "🚨 ВИСОКИЙ РІВЕНЬ АНОМАЛІЙ: Можливе перевантаження або атака на мережу."
            )
        elif total_anomalies > 10:
            results["recommendations"].append(
                "⚠️ СЕРЕДНІЙ РІВЕНЬ АНОМАЛІЙ: Виявлено помірну аномальну активність."
            )
        elif total_anomalies > 0:
            results["recommendations"].append(
                "ℹ️ НИЗЬКИЙ РІВЕНЬ АНОМАЛІЙ: Невеликі відхилення в трафіку."
            )
        else:
            results["recommendations"].append("✅ НОРМА: Значних аномалій не виявлено.")

        # Додаткові рекомендації на основі діагностики
        main_cat = diagnosis["main_category"]

        if main_cat == "Q_DNS":
            results["recommendations"].append(
                "🔧 Перевірте налаштування DNS на роутері або змініть DNS-сервери (наприклад, 8.8.8.8, 1.1.1.1)."
            )

        if main_cat == "Q_IP_ADDRESSING":
            results["recommendations"].append(
                "🔧 Перевірте DHCP-сервер, конфігурацію IP-адрес та можливі конфлікти у локальній мережі."
            )

        if main_cat == "Q_PERFORMANCE":
            results["recommendations"].append(
                "📉 Перевірте, чи немає програм, що сильно завантажують канал (торенти, хмарні синхронізації тощо)."
            )

        if main_cat == "Q_SECURITY":
            results["recommendations"].append(
                "🛡️ Перевірте підозрілі підключення, оновіть паролі та переконайтеся, що мережа захищена."
            )

        if main_cat == "Q_EXTERNAL":
            results["recommendations"].append(
                "🌐 Ймовірна проблема на стороні провайдера або віддалених серверів. "
                "Спробуйте перевірити інтернет з іншого пристрою або зверніться до підтримки провайдера."
            )

        print("✅ Вейвлет-аналіз завершено успішно!")
        return results

    except Exception as e:
        return {"error": f"Помилка аналізу: {str(e)}"}
