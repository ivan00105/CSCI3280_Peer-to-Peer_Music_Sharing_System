import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import Qt, QIODevice
from PyQt5.QtNetwork import QTcpSocket

class FileSender(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.file_path = None

    def init_ui(self):
        self.setWindowTitle('File Sender')
        self.setGeometry(300, 300, 300, 150)

        # Create widgets
        self.label = QLabel('Select a file to send.')
        self.btn_select_file = QPushButton('Select File')
        self.btn_send_file = QPushButton('Send File')

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_select_file)
        layout.addWidget(self.btn_send_file)

        # Set layout
        self.setLayout(layout)

        # Connect signals to slots
        self.btn_select_file.clicked.connect(self.select_file)
        self.btn_send_file.clicked.connect(self.send_file)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName()
        if file_path:
            self.file_path = file_path
            self.label.setText(f'Selected file: {file_path}')
        else:
            self.label.setText('No file selected.')

    def send_file(self):
        if not self.file_path:
            self.label.setText('Please select a file first.')
            return

        # Connect to remote PC using IP address and port
        ip_address = '192.168.100.4'  # Replace with the actual IP address of the remote PC
        port = 5000  # Replace with the desired port number
        socket = QTcpSocket()

        # Send file data
        with open(self.file_path, 'rb') as file:
            if socket.connectToHost(ip_address, port, QIODevice.WriteOnly):
                while True:
                    chunk = file.read(1024)
                    if not chunk:
                        break
                    socket.write(chunk)
                socket.waitForBytesWritten(3000)
                self.label.setText('File sent successfully.')
            else:
                self.label.setText('Failed to connect to the remote PC.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileSender()
    window.show()
    sys.exit(app.exec_())
