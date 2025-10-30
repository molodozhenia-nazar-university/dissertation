from scapy.all import rdpcap, TCP, UDP, ICMP, DNS, ARP, IP, IPv6, Raw, Ether
from scapy.layers.http import HTTPRequest, HTTPResponse

pcap_packets = []


def download_packets(file_path):
    """
    Завантажує пакети з pcap і повертає список словників із ключами:
    No, Time, Source, Destination, Protocol, Length, Info
    """
    global pcap_packets
    pcap_packets = rdpcap(file_path)

    packets_summary = []

    start_time = getattr(pcap_packets[0], "time", 0) if len(pcap_packets) > 0 else 0

    for i, pkt in enumerate(pcap_packets):
        try:
            timestamp = getattr(pkt, "time", 0)
            rel_time = timestamp - start_time
            length = len(pkt)
            proto = "OTHER"
            src = dst = "-"
            info = ""

            # --- IP / IPv6
            if IP in pkt:
                src = pkt[IP].src
                dst = pkt[IP].dst
            elif IPv6 in pkt:
                src = pkt[IPv6].src
                dst = pkt[IPv6].dst
            elif ARP in pkt:
                src = pkt[ARP].psrc
                dst = pkt[ARP].pdst
                proto = "ARP"
                info = "Who has {}? Tell {}".format(dst, src)

            # --- Protocols
            if TCP in pkt:
                proto = "TCP"
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport
                info = f"{sport} → {dport}"
                if pkt[TCP].flags:
                    info += f" [{pkt[TCP].flags}]"

                if pkt.haslayer(HTTPRequest):
                    proto = "HTTP"
                    info = f"{pkt[HTTPRequest].Method.decode()} {pkt[HTTPRequest].Host.decode()}{pkt[HTTPRequest].Path.decode()}"
                elif pkt.haslayer(HTTPResponse):
                    proto = "HTTP"
                    info = f"Response {pkt[HTTPResponse].Status_Code} {pkt[HTTPResponse].Reason_Phrase.decode(errors='ignore')}"

                elif Raw in pkt:
                    load = pkt[Raw].load[:40]
                    if b"TLS" in load or b"SSL" in load:
                        proto = "TLS"
                    elif b"SSH" in load:
                        proto = "SSH"
                    elif b"FTP" in load:
                        proto = "FTP"

            elif UDP in pkt:
                proto = "UDP"
                sport = pkt[UDP].sport
                dport = pkt[UDP].dport
                info = f"{sport} → {dport}"

                if DNS in pkt:
                    proto = "DNS"
                    if pkt[DNS].qd:
                        qname = pkt[DNS].qd.qname.decode(errors="ignore")
                        info = f"Standard query: {qname}"

                elif Raw in pkt:
                    load = pkt[Raw].load[:50]
                    if b"DHCP" in load:
                        proto = "DHCP"
                    elif b"MDNS" in load:
                        proto = "MDNS"
                    elif b"SSDP" in load:
                        proto = "SSDP"

            elif ICMP in pkt:
                proto = "ICMP"
                info = pkt.summary()

            elif Ether in pkt and proto == "OTHER":
                if pkt[Ether].type == 0x0806:
                    proto = "ARP"
                info = pkt.summary()

            packets_summary.append(
                {
                    "№": i + 1,
                    "Time": f"{rel_time:.6f}",
                    "Source": src,
                    "Destination": dst,
                    "Protocol": proto,
                    "Length": length,
                    "Information": info,
                }
            )

        except Exception as e:
            packets_summary.append(
                {
                    "№": i + 1,
                    "Time": "ERR",
                    "Source": "-",
                    "Destination": "-",
                    "Protocol": "ERROR",
                    "Length": 0,
                    "Information": str(e),
                }
            )

    return packets_summary


def get_details(index):
    pkt = pcap_packets[index]
    details = pkt.show(dump=True)
    return details
