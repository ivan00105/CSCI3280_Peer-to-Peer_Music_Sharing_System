# server.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QTextEdit, QLineEdit, QVBoxLayout
import socket

class ServerWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create the UI
        self.button = QPushButton("Receive")
        self.button.clicked.connect(self.receive_file)
        self.filename_label = QLabel("File name:")
        self.filename_edit = QLineEdit()
        self.text_edit = QTextEdit()

        # Layout the UI
        layout = QVBoxLayout()
        layout.addWidget(self.filename_label)
        layout.addWidget(self.filename_edit)
        layout.addWidget(self.button)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        # Create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("", 5000))
        self.sock.listen(5)

    def receive_file(self):
        # Accept a connection
        connection, address = self.sock.accept()

        # Get the file name
        filename = connection.recv(1024).decode()

        # Open the file for writing
        with open(filename, "wb") as f:
            data = connection.recv(1024)
            while data:
                f.write(data)
                data = connection.recv(1024)

        # Close the connection
        connection.close()

        # Update the UI
        self.filename_edit.setText(filename)
        self.text_edit.setText("Received file: " + filename)


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)

    # Create the window
    window = ServerWindow()

    # Show the window
    window.show()

    # Run the application
    sys.exit(app.exec_())
