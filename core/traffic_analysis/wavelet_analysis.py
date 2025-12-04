import numpy
import pywt
import warnings

from scapy.all import rdpcap, TCP, UDP, ICMP, DNS

warnings.filterwarnings("ignore")

from core.traffic_analysis.traffic_analysis_information import set_packets
from core.traffic_analysis.traffic_analysis_information import set_packets_information
from core.traffic_analysis.traffic_analysis_information import build_packets_information


def wavelet_analysis(file_path, wavelet_type="db4", level=6, interval_sec=1):

    def extract_traffic_features(packets):

        timestamps = []
        sizes = []
        protocols = []

        for packet in packets:
            if hasattr(packet, "time"):
                timestamps.append(float(packet.time))
            if hasattr(packet, "len"):
                sizes.append(int(packet.len))

            # Визначення протоколу
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
        """Створити часові ряди трафіку"""
        if not timestamps:
            return numpy.array([]), numpy.array([])

        start_time = min(timestamps)
        end_time = max(timestamps)

        # Створення часових інтервалів
        time_bins = numpy.arange(start_time, end_time + interval_sec, interval_sec)

        # Об'єм трафіку за інтервал
        traffic_volume = numpy.zeros(len(time_bins) - 1)
        packet_count = numpy.zeros(len(time_bins) - 1)

        for i, (ts, size) in enumerate(zip(timestamps, sizes)):
            bin_idx = int((ts - start_time) // interval_sec)
            if 0 <= bin_idx < len(traffic_volume):
                traffic_volume[bin_idx] += size
                packet_count[bin_idx] += 1

        return traffic_volume, packet_count

    def detect_anomalies_wavelet(signal, wavelet="db4", level=6, threshold_std=3.0):
        """Виявлення аномалій за допомогою вейвлет-аналізу Добеші"""
        if len(signal) < 2**level:
            # Якщо сигнал закороткий, зменшити рівень
            level = max(1, int(numpy.log2(len(signal))) - 1)

        try:
            # Вейвлет-розкладання
            coeffs = pywt.wavedec(signal, wavelet, level=level)

            anomalies = {
                "high_freq_anomalies": [],
                "low_freq_anomalies": [],
                "trend_breaks": [],
                "spikes": [],
            }

            # Аналіз деталізуючих коефіцієнтів (високочастотні компоненти)
            detail_coeffs = coeffs[1:]  # Всі крім апроксимуючих

            for i, detail in enumerate(detail_coeffs):
                if len(detail) > 0:
                    # Стандартне відхилення для поточного рівня
                    std_level = numpy.std(detail)
                    mean_level = numpy.mean(detail)

                    # Виявлення викидів
                    outliers = numpy.where(
                        numpy.abs(detail - mean_level) > threshold_std * std_level
                    )[0]

                    for outlier_idx in outliers:
                        time_position = outlier_idx * (2 ** (i + 1))
                        magnitude = detail[outlier_idx]

                        anomalies["high_freq_anomalies"].append(
                            {
                                "time_position": time_position,
                                "magnitude": magnitude,
                                "level": i + 1,
                                "type": "HIGH_FREQ",
                            }
                        )

            # Аналіз апроксимуючих коефіцієнтів (низькочастотні компоненти)
            approx_coeffs = coeffs[0]
            if len(approx_coeffs) > 10:
                std_approx = numpy.std(approx_coeffs)
                mean_approx = numpy.mean(approx_coeffs)

                # Виявлення змін тренду
                trend_changes = numpy.where(
                    numpy.abs(approx_coeffs - mean_approx) > 2 * std_approx
                )[0]

                for change_idx in trend_changes:
                    anomalies["low_freq_anomalies"].append(
                        {
                            "time_position": change_idx * (2**level),
                            "magnitude": approx_coeffs[change_idx],
                            "type": "TREND_CHANGE",
                        }
                    )

            return anomalies, coeffs

        except Exception as e:
            print(f"Помилка вейвлет-аналізу: {e}")
            return {}, []

    def analyze_protocol_anomalies(protocols, timestamps):
        """Аналіз аномалій у розподілі протоколів"""
        protocol_counts = {}
        protocol_timelines = {}

        for proto, ts in zip(protocols, timestamps):
            if proto not in protocol_counts:
                protocol_counts[proto] = 0
                protocol_timelines[proto] = []
            protocol_counts[proto] += 1
            protocol_timelines[proto].append(ts)

        anomalies = []

        # Аналіз раптових змін у протоколах
        for proto, times in protocol_timelines.items():
            if len(times) > 10:
                time_diff = numpy.diff(sorted(times))
                if len(time_diff) > 0:
                    avg_interval = numpy.mean(time_diff)
                    std_interval = numpy.std(time_diff)

                    # Виявлення спалахів активності
                    bursts = numpy.where(time_diff < avg_interval - 2 * std_interval)[0]
                    if len(bursts) > len(time_diff) * 0.3:  # Якщо більше 30% - аномалія
                        anomalies.append(
                            {
                                "type": "PROTOCOL_BURST",
                                "protocol": proto,
                                "burst_count": len(bursts),
                                "severity": (
                                    "HIGH"
                                    if len(bursts) > len(time_diff) * 0.5
                                    else "MEDIUM"
                                ),
                            }
                        )

        return anomalies, protocol_counts

    # ОСНОВНА ЛОГІКА ФУНКЦІЇ
    try:
        print(f"📖 Читання PCAP файлу: {file_path}")
        packets = rdpcap(file_path)

        if len(packets) == 0:
            return {"error": "Файл не містить пакетів"}

        print(f"📦 Обробка {len(packets)} пакетів...")

        set_packets(packets)

        set_packets_information(build_packets_information(packets))

        # Виділення характеристик трафіку
        timestamps, sizes, protocols = extract_traffic_features(packets)

        # Створення часових рядів
        traffic_volume, packet_count = create_time_series(timestamps, sizes)

        if len(traffic_volume) == 0:
            return {"error": "Не вдалося створити часові ряди"}

        # Нормалізація даних
        traffic_normalized = (traffic_volume - numpy.mean(traffic_volume)) / numpy.std(
            traffic_volume
        )
        packet_normalized = (packet_count - numpy.mean(packet_count)) / numpy.std(
            packet_count
        )

        # ВЕЙВЛЕТ-АНАЛІЗ
        print("🔍 Виконання вейвлет-аналізу Добеші ДБ4...")

        # Аналіз об'єму трафіку
        volume_anomalies, volume_coeffs = detect_anomalies_wavelet(
            traffic_normalized, wavelet_type, level
        )

        # Аналіз кількості пакетів
        packet_anomalies, packet_coeffs = detect_anomalies_wavelet(
            packet_normalized, wavelet_type, level
        )

        # Аналіз протоколів
        protocol_anomalies, protocol_stats = analyze_protocol_anomalies(
            protocols, timestamps
        )

        # ФОРМУВАННЯ РЕЗУЛЬТАТІВ
        results = {
            "summary": {
                "total_packets": len(packets),
                "analysis_duration": f"{len(traffic_volume)} інтервалів",
                "wavelet_type": wavelet_type,
                "wavelet_level": level,
            },
            "traffic_stats": {
                "total_volume": sum(sizes),
                "avg_packet_size": numpy.mean(sizes) if sizes else 0,
                "time_range": f"{min(timestamps) if timestamps else 0:.1f} - {max(timestamps) if timestamps else 0:.1f} сек",
            },
            "protocol_distribution": protocol_stats,
            "detected_anomalies": {
                "volume_anomalies": len(
                    volume_anomalies.get("high_freq_anomalies", [])
                ),
                "packet_anomalies": len(
                    packet_anomalies.get("high_freq_anomalies", [])
                ),
                "protocol_anomalies": len(protocol_anomalies),
                "trend_changes": len(volume_anomalies.get("low_freq_anomalies", [])),
            },
            "detailed_findings": {
                "high_frequency_spikes": volume_anomalies.get(
                    "high_freq_anomalies", []
                ),
                "traffic_trend_changes": volume_anomalies.get("low_freq_anomalies", []),
                "protocol_bursts": protocol_anomalies,
            },
            "recommendations": [],
        }

        # ФОРМУВАННЯ РЕКОМЕНДАЦІЙ
        total_anomalies = (
            results["detected_anomalies"]["volume_anomalies"]
            + results["detected_anomalies"]["packet_anomalies"]
            + results["detected_anomalies"]["protocol_anomalies"]
        )

        if total_anomalies > 20:
            results["recommendations"].append(
                "🚨 ВИСОКИЙ РІВЕНЬ ЗАГРОЗ: Можлива DDoS атака або масована аномальна активність"
            )
        elif total_anomalies > 10:
            results["recommendations"].append(
                "⚠️ СЕРЕДНІЙ РІВЕНЬ: Виявлено помірну аномальну активність"
            )
        elif total_anomalies > 0:
            results["recommendations"].append("ℹ️ НИЗЬКИЙ РІВЕНЬ: Незначні аномалії")
        else:
            results["recommendations"].append("✅ НОРМА: Аномалій не виявлено")

        # Додаткові рекомендації
        if results["detected_anomalies"]["protocol_anomalies"] > 0:
            results["recommendations"].append(
                "🔍 Перевірте підозрілу протокольну активність"
            )

        if results["detected_anomalies"]["trend_changes"] > 2:
            results["recommendations"].append("📈 Виявлені різкі зміни тренду трафіку")

        print("✅ Вейвлет-аналіз завершено успішно!")
        return results

    except Exception as e:
        return {"error": f"Помилка аналізу: {str(e)}"}
