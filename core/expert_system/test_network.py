def check_ping():
    # Твоя реалізація
    return {
        "description": "Ping перевірка пройшла успішно",
        "next_chat_id": "Q_IP_CONFIG",
    }


def check_ping_and_speed_test():
    # Твоя реалізація
    return {
        "description": "Швидкість низька, ping високий",
        "next_chat_id": "Q_NETWORK_CONGESTION",
    }


def check_special_ping():
    # Твоя реалізація
    return {"description": "Сайт доступний за IP", "next_chat_id": "Q_DNS"}
