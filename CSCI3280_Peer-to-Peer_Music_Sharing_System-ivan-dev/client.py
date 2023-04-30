# client.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QLineEdit, QVBoxLayout
import socket

class ClientWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create the UI
        self.button = QPushButton("Send")
        self.button.clicked.connect(self.send_file)
        self.filename_label = QLabel("File name:")
        self.filename_edit = QLineEdit()

        # Layout the UI
        layout = QVBoxLayout()
        layout.addWidget(self.filename_label)
        layout.addWidget(self.filename_edit)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # Connect to the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", 5000))

    def send_file(self):
        # Get the file name
        filename = self.filename_edit.text()

        # Send the file name to the server
        self.sock.sendall(filename.encode())

        # Receive the file from the server
        with open(filename, "wb") as f:
            data = self.sock.recv(1024)
            while data:
                f.write(data)
                data = self.sock.recv(1024)

        # Close the socket
        self.sock.close()


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)

    # Create the window
    window = ClientWindow()

    # Show the window
    window.show()

    # Run the application
    sys.exit(app.exec_())
