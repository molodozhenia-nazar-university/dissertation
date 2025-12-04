from scapy.all import rdpcap, TCP, UDP, ICMP, DNS, ARP, IP, IPv6, Raw, Ether
from scapy.layers.http import HTTPRequest, HTTPResponse

import sys
from io import StringIO
from scapy.utils import hexdump

# scapy — бібліотека для роботи з мережевими пакетами тощо.

# rdpcap — функція для читання файлів .pcap/.pcapng
# Вона повертає список пакетів, кожен з яких можна аналізувати окремо.

# TCP (Transmission Control Protocol)
# Протокол, який забезпечує надійну передачу даних у мережі (наприклад, HTTP, HTTPS, FTP, SSH).

# UDP (User Datagram Protocol)
# Протокол для швидкої, але менш надійної передачі даних (без підтверджень).

# ICMP (Internet Control Message Protocol)
# Використовується для службових повідомлень у мережі.
# Наприклад, команда "ping" працює саме через ICMP.

# DNS (Domain Name System)
# Протокол, який перетворює доменне ім’я (наприклад, google.com) у IP-адресу (наприклад, 111.250.111.200).

# ARP (Address Resolution Protocol)
# Використовується всередині локальної мережі для отримання MAC-адреси пристрою за його IP-адресою.

# IP (Internet Protocol, версія 4)
# Основний мережевий протокол, який визначає адресу пристрою в мережі (IPv4).

# IPv6 (Internet Protocol, версія 6)
# Новіша версія IP з більшим простором адрес (для сучасних мереж).

# Raw (сирі дані)
# Використовується, коли пакет містить необроблену частину даних (payload), яку scapy не може розпізнати як відомий протокол.

# Ether (Ethernet)
# Найнижчий рівень мережі — описує фізичний кадр у локальній мережі (MAC-адреси).

# HTTPRequest
# Визначає HTTP-запит від клієнта до сервера (наприклад, GET або POST).

# HTTPResponse
# Визначає HTTP-відповідь від сервера (наприклад, "200 OK", "404 Not Found").

packets = []
packets_information = []


def set_packets(new_packets):
    global packets
    packets = new_packets


def get_packets():
    return packets or []


def set_packets_information(build_packets_information):
    global packets_information
    packets_information = build_packets_information


def get_packets_information():
    return packets_information or []


def build_packets_information(packets):

    packets_information = []

    start_time = getattr(packets[0], "time", 0) if len(packets) > 0 else 0

    for i, packet in enumerate(packets):
        try:
            # Абсолютний час створення пакета.
            stop_time = getattr(packet, "time", 0)
            # Час відносно початку захоплення.
            time = stop_time - start_time
            # Довжина пакета у байтах.
            length = len(packet)

            protocol = "OTHER"
            source = destination = "-"
            information = ""

            if IP in packet:
                source = packet[IP].src
                destination = packet[IP].dst
            elif IPv6 in packet:
                source = packet[IPv6].src
                destination = packet[IPv6].dst
            elif ARP in packet:
                source = packet[ARP].psrc
                destination = packet[ARP].pdst
                protocol = "ARP"
                information = "Who has {}? Tell {}".format(destination, source)

            # --- Protocols
            if TCP in packet:
                protocol = "TCP"
                sport = packet[TCP].sport
                dport = packet[TCP].dport
                information = f"{sport} → {dport}"
                if packet[TCP].flags:
                    information += f" [{packet[TCP].flags}]"

                if packet.haslayer(HTTPRequest):
                    protocol = "HTTP"
                    information = f"{packet[HTTPRequest].Method.decode()} {packet[HTTPRequest].Host.decode()}{packet[HTTPRequest].Path.decode()}"
                elif packet.haslayer(HTTPResponse):
                    protocol = "HTTP"
                    information = f"Response {packet[HTTPResponse].Status_Code} {packet[HTTPResponse].Reason_Phrase.decode(errors='ignore')}"

                elif Raw in packet:
                    load = packet[Raw].load[:40]
                    if b"TLS" in load or b"SSL" in load:
                        protocol = "TLS"
                    elif b"SSH" in load:
                        protocol = "SSH"
                    elif b"FTP" in load:
                        protocol = "FTP"

            elif UDP in packet:
                protocol = "UDP"
                sport = packet[UDP].sport
                dport = packet[UDP].dport
                information = f"{sport} → {dport}"

                if DNS in packet:
                    protocol = "DNS"
                    if packet[DNS].qd:
                        qname = packet[DNS].qd.qname.decode(errors="ignore")
                        information = f"Standard query: {qname}"

                elif Raw in packet:
                    load = packet[Raw].load[:50]
                    if b"DHCP" in load:
                        protocol = "DHCP"
                    elif b"MDNS" in load:
                        protocol = "MDNS"
                    elif b"SSDP" in load:
                        protocol = "SSDP"

            elif ICMP in packet:
                protocol = "ICMP"
                information = packet.summary()

            elif Ether in packet and protocol == "OTHER":
                if packet[Ether].type == 0x0806:
                    protocol = "ARP"
                information = packet.summary()

            packets_information.append(
                {
                    "№": i + 1,
                    "Time": f"{time:.6f}",
                    "Source": source,
                    "Destination": destination,
                    "Protocol": protocol,
                    "Length": length,
                    "Information": information,
                }
            )

        except Exception as e:
            packets_information.append(
                {
                    "№": i + 1,
                    "Time": "ERROR",
                    "Source": "-",
                    "Destination": "-",
                    "Protocol": "ERROR",
                    "Length": 0,
                    "Information": str(e),
                }
            )

    return packets_information


def get_details(index):
    packet = packets[index]
    details = packet.show(dump=True)
    return details


def get_packet_layers(index):
    packet = packets[index]
    layers = {}
    while packet:
        layer = packet.name
        fields = {k: v for k, v in packet.fields.items()}
        layers[layer] = fields
        packet = packet.payload
    return layers


def get_packet_hexdump(index):
    packet = packets[index]
    # Перехоплюємо stdout, бо hexdump друкує у консоль.
    buffer = StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buffer
    try:
        hexdump(packet)
    finally:
        sys.stdout = sys_stdout

    return buffer.getvalue()
