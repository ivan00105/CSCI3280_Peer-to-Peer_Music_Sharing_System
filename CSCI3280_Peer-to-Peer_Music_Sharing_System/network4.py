import sys
import socket
import time
import threading

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class FileSharer(QWidget):

    def __init__(self):
        super().__init__()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", 5000))
        self.server_socket.listen(5)

        self.client_sockets = []

        self.file_list = QListWidget()
        self.send_button = QPushButton("Send")
        self.receive_button = QPushButton("Receive")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.file_list)
        self.layout.addWidget(self.send_button)
        self.layout.addWidget(self.receive_button)

        self.setLayout(self.layout)

        self.send_button.clicked.connect(self.send_file)
        self.receive_button.clicked.connect(self.receive_file)

        self.thread = threading.Thread(target=self.listen_for_connections)
        self.thread.start()

    def listen_for_connections(self):
        while True:
            connection, address = self.server_socket.accept()
            self.client_sockets.append(connection)

            thread = threading.Thread(target=self.handle_connection, args=(connection, address))
            thread.start()

    def handle_connection(self, connection, address):
        while True:
            data = connection.recv(1024)
            if not data:
                break

            print("Received data from {}: {}".format(address, data))

            if data == "send":
                filename, _ = QFileDialog.getOpenFileName(self, "Choose a file to send", "", "Text Files(*.txt)")
                with open(filename, "rb") as f:
                    connection.sendall(f.read())

            elif data == "receive":
                filename = input("Enter filename: ")
                with open(filename, "wb") as f:
                    data = connection.recv(1024)
                    while data:
                        f.write(data)
                        data = connection.recv(1024)

        connection.close()

    def send_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Choose a file to send", "", "All Files(*.*)")
        for client_socket in self.client_sockets:
            client_socket.sendall("send".encode())
            client_socket.sendall(filename.encode())

        with open(filename, "rb") as f:
            data = f.read()
            for client_socket in self.client_sockets:
                try:
                    client_socket.sendall(data)
                except Exception as e:
                    print(e)

    def receive_file(self):
        filename = input("Enter filename: ")
        for client_socket in self.client_sockets:
            client_socket.sendall("receive".encode())
            client_socket.sendall(filename.encode())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    sharer = FileSharer()
    sharer.show()

    sys.exit(app.exec_())
