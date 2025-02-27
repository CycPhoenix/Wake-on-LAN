import sys
from wakeonlan import send_magic_packet

def wake_pc(mac_address):
    """Sends a Wake-on-LAN magic packet to the given MAC address."""
    try:
        send_magic_packet(mac_address)
        print(f"Magic packet sent to {mac_address} ✅")
    except Exception as e:
        print(f"Error: {e} ❌")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python wol.py <MAC_ADDRESS>")
    else:
        mac_address = sys.argv[1]
        wake_pc(mac_address)