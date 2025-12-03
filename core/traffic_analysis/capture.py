import os
from scapy.all import conf
from threading import Thread

from core.traffic_analysis.capture_session import CaptureSession


def get_interfaces():

    dictionary_interfaces = {}

    for interface in conf.ifaces.values():

        name = str(interface.name)
        description = str(interface.description or "")
        mac = getattr(interface, "mac", None)
        ip = getattr(interface, "ip", None)

        lower_name = (name + description).lower()

        friendly_name = determine_friendly_name(lower_name)

        display_name = f"{friendly_name}"

        if ip:
            display_name += f"  —  {ip}"

        dictionary_interfaces[display_name] = name

    if not dictionary_interfaces:
        dictionary_interfaces[" Інтерфейси не знайдено "] = None

    return dictionary_interfaces


def determine_friendly_name(lower_name):

    # VPN Adapter
    if "tun" in lower_name or "tap" in lower_name or "vpn" in lower_name:
        return "VPN Adapter"

    # Windows Capture Adapter
    elif "npcap" in lower_name or "npf" in lower_name:
        return "Windows Capture Adapter"

    # Virtual Machine Adapter
    elif "vbox" in lower_name or "vmnet" in lower_name:
        return "Virtual Machine Adapter"

    # Docker / Container
    elif "docker" in lower_name or "br-" in lower_name:
        return "Docker/Container Adapter"

    # Wi-Fi
    elif "wlan" in lower_name or "wi-fi" in lower_name or "wireless" in lower_name:
        return "Wi-Fi"

    # Ethernet
    elif "eth" in lower_name or "ethernet" in lower_name or "lan" in lower_name:
        return "Ethernet"

    # Loopback
    elif "lo" in lower_name or "loopback" in lower_name:
        return "Loopback"

    # Mobile / Cellular
    elif "wwan" in lower_name or "cellular" in lower_name or "mobile" in lower_name:
        return "Mobile/Cellular"

    # Other
    else:
        return "Інший адаптер"


def generate_unique_capture_filename(
    folder="live_traffic", base_name="live_traffic", ext=".pcap"
):
    os.makedirs(folder, exist_ok=True)

    index = 0
    while True:
        filename = f"{base_name}_{index}{ext}"
        full_path = os.path.join(folder, filename)
        if not os.path.exists(full_path):
            return full_path
        index += 1


def start_capture(
    interface,
    use_duration,
    duration,
    buffer_spin_mb,
    output_path,
    update_result_text,
    on_finished,
):
    capture_session = CaptureSession(
        interface,
        use_duration,
        duration,
        buffer_spin_mb,
        output_path,
        update_result_text,
        on_finished,
    )

    Thread(target=capture_session.start, daemon=True).start()

    return capture_session
