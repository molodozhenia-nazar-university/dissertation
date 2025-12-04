def format_analysis_results(results: dict) -> str:
    """
    Форматує результати аналізу у зручний для користувача текст.
    Використовує блоки:
      - summary
      - detected_anomalies
      - protocol_distribution
      - diagnosis
      - recommendations
    """

    # ---- Захист від помилок ----
    if "error" in results:
        return f"❌ Помилка аналізу: {results['error']}"

    summary = results.get("summary", {})
    anomalies = results.get("detected_anomalies", {})
    protocol_distribution = results.get("protocol_distribution", {})
    diagnosis = results.get(
        "diagnosis",
        {
            "main_category": "NONE",
            "severity": "LOW",
            "confidence": 1.0,
            "subcategories": [],
        },
    )
    diagnosis_aux = results.get("diagnosis_aux", {})

    # Мапінги кодів у «людські» назви
    category_names = {
        "Q_DNS": "DNS (служби іменування доменів)",
        "Q_IP_ADDRESSING": "IP-адресація та DHCP",
        "Q_PERFORMANCE": "Продуктивність та стабільність мережі",
        "Q_SECURITY": "Безпека та підозріла активність",
        "Q_EXTERNAL": "Зовнішні ресурси / провайдер",
        "NONE": "Суттєвих проблем не виявлено",
    }

    severity_names = {
        "LOW": "Низький",
        "MEDIUM": "Середній",
        "HIGH": "Високий",
        "CRITICAL": "Критичний",
    }

    main_category_code = diagnosis.get("main_category", "NONE")
    main_category_name = category_names.get(main_category_code, main_category_code)
    severity_code = diagnosis.get("severity", "LOW")
    severity_name = severity_names.get(severity_code, severity_code)
    confidence = float(diagnosis.get("confidence", 0.0))

    # --------- Базова інформація ---------
    result_string = f"""✅ Аналіз завершено!

📊 ЗАГАЛЬНА СТАТИСТИКА:
• Пакетів проаналізовано: {summary.get('total_packets', '—')}
• Тривалість аналізу: {summary.get('analysis_duration', '—')}
• Вейвлет: {summary.get('wavelet_type', '—')} (рівень {summary.get('wavelet_level', '—')})

🩺 ПОПЕРЕДНІЙ ДІАГНОЗ:
• Основна категорія проблеми: {main_category_name}
• Рівень серйозності: {severity_name}
• Впевненість у діагнозі: {confidence * 100:.0f}%
"""

    # --------- Деталізація діагнозу ---------
    subcategories = diagnosis.get("subcategories", [])
    if subcategories:
        result_string += "\n📌 Деталізація виявлених проблем:\n"
        # не будемо спамити, візьмемо топ-3
        for issue in subcategories[:3]:
            cat_code = issue.get("category", "")
            cat_name = category_names.get(cat_code, cat_code)
            issue_conf = float(issue.get("confidence", 0.0)) * 100
            user_message = issue.get("user_message", "").strip()
            result_string += (
                f"• [{cat_name}] {user_message} (ймовірність ≈ {issue_conf:.0f}%)\n"
            )

    # --------- Короткий технічний зріз по категоріях ---------
    dns_metrics = diagnosis_aux.get("dns", {})
    ip_metrics = diagnosis_aux.get("ip_addressing", {})
    security_metrics = diagnosis_aux.get("security", {})
    external_metrics = diagnosis_aux.get("external", {})

    # DNS
    if dns_metrics.get("total_queries", 0) > 0:
        result_string += "\n🔎 DNS (служби іменування):\n"
        result_string += (
            f"• DNS-запитів: {dns_metrics.get('total_queries', 0)}, "
            f"помилкових/без відповіді: "
            f"{dns_metrics.get('error_responses', 0) + dns_metrics.get('unanswered_queries', 0)} "
            f"({dns_metrics.get('failure_rate', 0.0) * 100:.0f}%)\n"
        )

    # IP-адресація
    if any(
        ip_metrics.get(k, 0) > 0
        for k in ("dhcp_discover", "dhcp_offer", "dhcp_ack", "dhcp_request")
    ):
        result_string += "\n🧩 IP-адресація (DHCP / ARP):\n"
        result_string += (
            f"• DHCP DISCOVER: {ip_metrics.get('dhcp_discover', 0)}, "
            f"OFFER: {ip_metrics.get('dhcp_offer', 0)}, "
            f"REQUEST: {ip_metrics.get('dhcp_request', 0)}, "
            f"ACK: {ip_metrics.get('dhcp_ack', 0)}\n"
        )
        if ip_metrics.get("ip_conflicts"):
            result_string += (
                "• Виявлено можливі конфлікти IP-адрес (одна IP з кількома MAC).\n"
            )

    # Безпека
    if security_metrics.get("syn_total", 0) > 0:
        result_string += "\n🛡️ Безпека трафіку:\n"
        result_string += (
            f"• SYN-пакетів (спроб підключення): {security_metrics.get('syn_total', 0)}, "
            f"без відповіді SYN+ACK: {security_metrics.get('syn_no_ack', 0)} "
            f"({security_metrics.get('syn_no_ack_ratio', 0.0) * 100:.0f}%)\n"
        )
        if security_metrics.get("port_scan_sources"):
            result_string += "• Виявлені джерела, що сканують порти (багато підключень до різних портів).\n"

    # Зовнішні ресурси
    if external_metrics.get("external_syn", 0) > 0:
        result_string += "\n🌐 Підключення до зовнішніх ресурсів:\n"
        result_string += (
            f"• Спроб підключення до зовнішніх IP (SYN): {external_metrics.get('external_syn', 0)}, "
            f"невдалих: {external_metrics.get('external_failed', 0)} "
            f"({external_metrics.get('external_failure_ratio', 0.0) * 100:.0f}%)\n"
        )

    # --------- Аномалії ---------
    result_string += "\n🚨 ВИЯВЛЕНІ АНОМАЛІЇ (за вейвлет-аналізом):\n"
    result_string += f"• Спайків трафіку: {anomalies.get('volume_anomalies', 0)}\n"
    result_string += (
        f"• Аномалій за кількістю пакетів: {anomalies.get('packet_anomalies', 0)}\n"
    )
    result_string += (
        f"• Протокольних аномалій: {anomalies.get('protocol_anomalies', 0)}\n"
    )
    result_string += (
        f"• Різких змін тренду трафіку: {anomalies.get('trend_changes', 0)}\n"
    )

    # --------- Розподіл протоколів ---------
    result_string += "\n📈 РОЗПОДІЛ ПРОТОКОЛІВ:\n"
    if protocol_distribution:
        for protocol, count in protocol_distribution.items():
            result_string += f"• {protocol}: {count} пакетів\n"
    else:
        result_string += "• Дані відсутні\n"

    # --------- Рекомендації ---------
    result_string += "\n💡 РЕКОМЕНДАЦІЇ ДЛЯ КОРИСТУВАЧА:\n"
    recommendations = results.get("recommendations", [])
    if recommendations:
        for recommendation in recommendations:
            result_string += f"• {recommendation}\n"
    else:
        result_string += "• Додаткових рекомендацій немає.\n"

    return result_string
