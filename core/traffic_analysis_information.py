from scapy.all import rdpcap, TCP, UDP, ICMP, DNS

pcap_packets = []


def download_packets(file_path):
    global pcap_packets
    pcap_packets = rdpcap(file_path)
    summary_list = []
    for i, pkt in enumerate(pcap_packets):
        ts = getattr(pkt, "time", 0)
        proto = "OTHER"
        if pkt.haslayer(TCP):
            proto = "TCP"
        elif pkt.haslayer(UDP):
            proto = "UDP"
        elif pkt.haslayer(ICMP):
            proto = "ICMP"
        elif pkt.haslayer(DNS):
            proto = "DNS"
        summary_list.append(f"{i+1:04d} | {ts:.3f} | {proto} | {len(pkt)} bytes")
    return summary_list


def get_details(index):
    pkt = pcap_packets[index]
    details = pkt.show(dump=True)
    return details
