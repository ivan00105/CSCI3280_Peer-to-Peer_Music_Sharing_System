import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtNetwork import QTcpSocket

class FileSender(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('File Sender')
        self.setGeometry(300, 300, 300, 150)

        # Create widgets
        self.label = QLabel()
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
        self.label.setText(f'Selected file: {file_path}')
        self.file_path = file_path

    def send_file(self):
        if hasattr(self, 'file_path'):
            try:
                # Connect to remote PC using IP address and port
                ip_address = '192.168.100.4'  # Replace with the actual IP address of the remote PC
                port = 5000  # Replace with the desired port number
                socket = QTcpSocket()
                socket.connectToHost(ip_address, port)

                if socket.waitForConnected(3000):
                    # Send file data
                    with open(self.file_path, 'rb') as file:
                        while True:
                            chunk = file.read(1024)
                            if not chunk:
                                break
                            socket.write(chunk)
                        socket.flush()
                    socket.waitForBytesWritten(3000)
                    socket.disconnectFromHost()
                    self.label.setText('File sent successfully.')
                else:
                    self.label.setText('Failed to connect to the remote PC.')
            except Exception as e:
                self.label.setText(f'Error: {e}')
        else:
            self.label.setText('Please select a file first.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileSender()
    window.show()
    sys.exit(app.exec_())



