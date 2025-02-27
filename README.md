# Wake-on-WAN Tool 🚀

A lightweight Wake-on-WAN (WoWAN) tool that allows users to remotely wake up their computers **from anywhere over the internet**, using a custom PyQt6 interface.

## 🌟 Features
- Wake up a PC over **LAN & WAN** (local network or internet).
- Supports **custom Dynamic DNS (DDNS)** (No-IP, DuckDNS).
- Saves **favorite MAC addresses** for quick access.
- Logs **wake-up attempts** with timestamps.
- Simple and modern **PyQt6 GUI**.

## 🛠️ Installation
1. Install Python:
```bash
python --version
```
2. Install dependencies:
```bash
pip install wakeonlan pyqt6
```
3. Run the script:
```bash
python wol_gui.py
```

## 🌐 Setting Up Wake-on-WAN
1. **Enable Wake-on-LAN (WoL) in BIOS.**
2. **Configure your router for Port Forwarding:**
- **Protocol**: UDP
- **Port**: 9
- **Destination IP**: Your PC's internal IP
3. **Set up a Dynamic DNS (DDNS) service** (if you don't have a static IP).
4. **Modify the script to use your public IP/DDNS.**

## 🔧 Future Enhancements
- Improved UI with **system tray support**.
- Customizable **network settings (ports, broadcast options)**
- mobile app integration for **remote wake-up on the go**.

## 🤝 Contributors
Feel free to contribute! Open an issue or submit a pull request.

## 📜 License
This project is licensed under the [MIT License](https://github.com/CycPhoenix/Wake-on-WAN?tab=MIT-1-ov-file).