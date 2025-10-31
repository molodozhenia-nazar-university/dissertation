from scapy.all import sniff, wrpcap, conf
from threading import Thread


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


def start_capture(interface, duration, output_path, update_status_result):
    def capture_thread():
        try:
            update_status_result(f"🔍 Початок захоплення з {interface}...")
            packets = sniff(
                iface=interface,
                timeout=duration,
            )
            wrpcap(output_path, packets)
            update_status_result(f"✅ Захоплено {len(packets)} пакетів.")
            update_status_result(f"💾 Збережено у файл: {output_path}")
        except Exception as e:
            update_status_result(f"❌ Помилка захоплення: {e}")

    Thread(target=capture_thread, daemon=True).start()
