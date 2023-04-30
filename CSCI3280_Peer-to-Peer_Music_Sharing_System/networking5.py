import sys
import socket
import struct
import time
import threading
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class AudioFileSharer(QMainWindow):

    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.list_of_connected_devices = QListWidget()
        self.list_of_available_files = QListWidget()

        self.send_button = QPushButton("Send")
        self.receive_button = QPushButton("Receive")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list_of_connected_devices)
        self.layout.addWidget(self.list_of_available_files)
        self.layout.addWidget(self.send_button)
        self.layout.addWidget(self.receive_button)

        self.central_widget.setLayout(self.layout)

        self.send_button.clicked.connect(self.send_file)
        self.receive_button.clicked.connect(self.receive_file)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", 5000))
        self.socket.listen(5)

        self.connected_devices = []
        self.available_files = []

        self.thread = threading.Thread(target=self.listen_for_connections)
        self.thread.start()

    def listen_for_connections(self):
        while True:
            connection, address = self.socket.accept()
            self.connected_devices.append(address)
            self.list_of_connected_devices.addItem(address)

            self.send_file_to_device(connection)

    def send_file_to_device(self, connection):
        file_name = QFileDialog.getOpenFileName(self, "Select a file to send")
        if file_name:
            with open(file_name, "rb") as f:
                file_size = os.path.getsize(file_name)
                connection.sendall(struct.pack("!L", file_size))
                connection.sendall(f.read(file_size))

    def receive_file(self):
        device_address = self.list_of_connected_devices.currentItem().text()
        file_name, file_size = self.receive_file_from_device(device_address)

        with open(file_name, "wb") as f:
            f.write(self.receive_file_from_device(device_address))

    def receive_file_from_device(self, device_address):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((device_address, 5001))

        file_size = struct.unpack("!L", connection.recv(4))[0]

        file_data = b""
        while file_size > 0:
            data = connection.recv(file_size)
            file_data += data
            file_size -= len(data)

        return file_data, file_size


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = AudioFileSharer()
    main_window.show()

    sys.exit(app.exec_())
