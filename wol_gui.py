import sys
import json
import socket
import datetime
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget, QComboBox
from wakeonlan import send_magic_packet

FAVORITES_FILE = "mac_addresses.json"
LOG_FILE = "wol_log.txt"

class WakeOnWanApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wake-on-WAN Tool")
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()

        self.label = QLabel("Enter MAC Address:")
        self.mac_input = QLineEdit()
        self.wake_button = QPushButton("Wake PC")

        self.network_mode_label = QLabel("Select Mode:")
        self.network_mode = QComboBox()
        self.network_mode.addItems(["LAN", "WAN"])

        self.ip_label = QLabel("Public IP / DDNS:")
        self.ip_input = QLineEdit("yourname.ddns.net")

        self.favorites_list = QListWidget()
        self.add_fav_button = QPushButton("Add to Favorites")
        self.remove_fav_button = QPushButton("Remove Selected")

        self.view_logs_button = QPushButton("View_Logs")

        layout.addWidget(self.label)
        layout.addWidget(self.mac_input)
        layout.addWidget(self.network_mode_label)
        layout.addWidget(self.network_mode)
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)
        layout.addWidget(self.wake_button)
        layout.addWidget(QLabel("Favorite MAC Addresses:"))
        layout.addWidget(self.favorites_list)
        layout.addWidget(self.add_fav_button)
        layout.addWidget(self.remove_fav_button)
        layout.addWidget(self.view_logs_button)

        self.wake_button.clicked.connect(self.wake_pc)
        self.add_fav_button.clicked.connect(self.add_favorite)
        self.remove_fav_button.clicked.connect(self.remove_favorite)
        self.favorites_list.itemClicked.connect(self.select_favorite)
        self.view_logs_button.clicked.connect(self.view_logs)

        self.setLayout(layout)
        self.load_favorites()

    def wake_pc(self):
        mac_address = self.mac_input.text()
        mode = self.network_mode.currentText()
        ip = self.ip_input.text() if mode == "WAN" else "255.255.255.255"

        if mac_address:
            try:
                self.send_wol_packet(mac_address, ip)
                self.log_attempt(mac_address, ip, mode, "SUCCESS ✅")
                QMessageBox.information(self, "Success", f"Magic packet sent to {mac_address} via {mode} ✅")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to send packet: {str(e)} ❌")
        else:
            QMessageBox.warning(self, "Error", "Please enter a MAC address ❌")

    def send_wol_packet(self, mac_address, ip ,port=9):
        mac_bytes = bytes.fromhex(mac_address.replace(":", "").replace("-", ""))
        magic_packet = b'\xff' * 6 + mac_bytes * 16

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(magic_packet, (ip, port))

    def log_attempts(self, mac, ip, mode, status):
        with open(LOG_FILE, "a") as log:
            log.write(f"[{datetime.datetime.now()}] {mode} Wake sent to {mac} via {ip} - {status}\n")

    def view_logs(self):
        try:
            with open(LOG_FILE, "r") as f:
                logs = f.read()
            QMessageBox.information(self, "Wake-on-WAN Logs", logs or "No logs yet.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No logs found.")

    def load_favorites(self):
        try:
            with open(FAVORITES_FILE, "r") as f:
                data = json.load(f)
                for entry in data.get("favorites", []):
                    self.favorites_list.addItem(f"{entry['name']} - {entry['mac']}")
        except FileNotFoundError:
            with open(FAVORITES_FILE, "w") as f:
                json.dump({"favorites": []}, f)

    def add_favorite(self):
        mac_address = self.mac_input.text()
        if mac_address:
            name, _ = QMessageBox.getText(self, "Save MAC", "Enter a name for this MAC address:")
            if name:
                with open(FAVORITES_FILE, "r+") as f:
                    data = json.load(f)
                    data["favorites"].append({"name": name, "mac": mac_address})
                    f.seek(0)
                    json.dump(data, f, indent=4)
                self.favorites_list.addItem(f"{name} - {mac_address}")
        else:
            QMessageBox.warning(self, "Error", "Enter a MAC address before adding to favorites ❌")

    def remove_favorite(self):
        selected_item = self.favorites_list.currentItem()
        if selected_item:
            mac_name = selected_item.text()
            with open(FAVORITES_FILE, "r+") as f:
                data = json.load(f)
                data["favorites"] = [entry for entry in data["favorites"] if f"{entry['name']} - {entry['mac']}" != mac_name]
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
            self.favorites_list.takeItem(self.favorites_list.row(selected_item))
        else:
            QMessageBox.warning(self, "Error", "Select a favorite to remove ❌")

    def select_favorite(self):
        selected_item = self.favorites_list.currentItem()
        if selected_item:
            mac_address = selected_item.text().split(" - ")[1]
            self.mac_input.setText(mac_address)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WakeOnWanApp()
    window.show()
    sys.exit(app.exec())
