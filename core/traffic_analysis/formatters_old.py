def format_analysis_results(results: dict) -> str:

    # To format analysis results
    result_string = f"""✅ Аналіз завершено!

📊 ЗАГАЛЬНА СТАТИСТИКА:
• Пакетів проаналізовано: {results['summary']['total_packets']}
• Тривалість аналізу: {results['summary']['analysis_duration']}
• Вейвлет: {results['summary']['wavelet_type']} (рівень {results['summary']['wavelet_level']})

🚨 ВИЯВЛЕНІ АНОМАЛІЇ:
• Спайків трафіку: {results['detected_anomalies']['volume_anomalies']}
• Аномалій пакетів: {results['detected_anomalies']['packet_anomalies']} 
• Протокольних аномалій: {results['detected_anomalies']['protocol_anomalies']}
• Змін тренду: {results['detected_anomalies']['trend_changes']}

📈 РОЗПОДІЛ ПРОТОКОЛІВ:
"""

    for protocol, count in results["protocol_distribution"].items():
        result_string += f"• {protocol}: {count} пакетів\n"

    result_string += "💡 РЕКОМЕНДАЦІЇ:\n"
    for recommendation in results["recommendations"]:
        result_string += f"• {recommendation}\n"

    return result_string
