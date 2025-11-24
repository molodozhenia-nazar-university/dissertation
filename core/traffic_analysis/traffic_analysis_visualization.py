from scapy.all import rdpcap, TCP, UDP, ICMP, DNS, ARP, IP, IPv6, Raw, Ether
from scapy.layers.http import HTTPRequest, HTTPResponse
from collections import Counter, defaultdict

import numpy
import matplotlib.pyplot as pyplot


def create_plot(file_path, visualization_name):

    packets = rdpcap(file_path)
    if not packets:
        figure, ax = pyplot.subplots()
        ax.text(0.5, 0.5, "Проблема!", ha="center", va="center")
        return figure

    figure, ax = pyplot.subplots(figsize=(10, 5))
    figure.subplots_adjust(bottom=0.10)

    # "Traffic over Time"
    if "Трафік у часі" in visualization_name:

        figure.suptitle("Трафік у часі", fontsize=20, fontweight="bold")

        time = [packet.time - packets[0].time for packet in packets]

        step = 1
        number_steps = int(time[-1]) + 1
        # bins - інтервали часу [number X, number Y]
        # counter - (список) кількість пакетів в інтервалі bin [number X, number Y]
        # edges - (список) межі інтервалу bin [number X, number Y]
        bins = numpy.arange(0, number_steps + step, step)

        counter, edges = numpy.histogram(time, bins=bins)

        # plot
        ax.plot(edges[:-1], counter, color="#3498DB")
        ax.set_xlabel("секунда")
        ax.set_ylabel("пакет / секунда")
        ax.grid(True, alpha=0.5)

        return figure

    # "Inbound vs Outbound Traffic"
    elif "Вхідний vs Вихідний трафік" in visualization_name:

        figure.suptitle("Вхідний vs Вихідний трафік", fontsize=20, fontweight="bold")

        local_ip = detect_local_ip(packets)

        inbound = 0
        outbound = 0

        for packet in packets:
            if IP in packet:
                source = packet[IP].src
                destination = packet[IP].dst
                if destination == local_ip:
                    inbound += 1
                elif source == local_ip:
                    outbound += 1

        ax.bar(
            ["Вхідний", "Вихідний"], [inbound, outbound], color=["#3498DB", "#28B463"]
        )
        ax.set_ylabel("кількість пакетів")

        return figure

    # "Top Talkers (Active IPs)"
    elif "Найактивніші IP" in visualization_name:

        figure.suptitle("Вхідний vs Вихідний трафік", fontsize=20, fontweight="bold")

        ips = []

        for packet in packets:
            if IP in packet:
                ips.append(packet[IP].src)
                ips.append(packet[IP].dst)
            elif IPv6 in packet:
                ips.append(packet[IPv6].src)
                ips.append(packet[IPv6].dst)

        if not ips:
            figure, ax = pyplot.subplots()
            ax.text(
                0.5, 0.5, "IP-трафіку не знайдено у файлі", ha="center", va="center"
            )
            return figure

        counter_ip = Counter(ips).most_common(10)
        ip_labels = [item[0] for item in counter_ip]  # Список IP-адрес
        ip_values = [item[1] for item in counter_ip]  # Кількість пакетів

        ax.barh(ip_labels, ip_values, color="#E67E22")
        ax.set_xlabel("кількість пакетів")
        ax.set_ylabel("ip-адреси")

        return figure

    # "Protocol Distribution" CHANGE
    elif "Розподіл протоколів" in visualization_name:

        return figure

    # CODE BUFFER

    # Empty
    else:
        figure, ax = pyplot.subplots()
        ax.text(0.5, 0.5, "ERROR", ha="center", va="center")
        return figure


def detect_local_ip(packets):

    ips = []

    for packet in packets:
        if IP in packet:
            ips.append(packet[IP].src)
            ips.append(packet[IP].dst)

    if not ips:
        return None

    return Counter(ips).most_common(1)[0][0]
