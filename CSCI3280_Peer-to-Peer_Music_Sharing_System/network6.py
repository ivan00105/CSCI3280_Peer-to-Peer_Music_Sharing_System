import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt

class AudioShareWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Audio File Sharing')
        self.setGeometry(100, 100, 500, 300)

        self.file_path = ''
        self.dest_ip = ''
        self.connected = False

        self.init_ui()

    def init_ui(self):
        self.select_file_btn = QPushButton('Select File', self)
        self.select_file_btn.move(50, 50)
        self.select_file_btn.clicked.connect(self.select_file)

        self.dest_ip_label = QLabel('Destination IP:', self)
        self.dest_ip_label.move(50, 100)

        self.dest_ip_input = QLineEdit(self)
        self.dest_ip_input.move(150, 100)

        self.connect_btn = QPushButton('Connect', self)
        self.connect_btn.move(50, 150)
        self.connect_btn.clicked.connect(self.connect)

        self.status_label = QLabel('Not connected', self)
        self.status_label.move(50, 200)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File', '', 'Audio Files (*.mp3 *.wav)')
        if file_path:
            self.file_path = file_path

    def connect(self):
        if not self.file_path:
            QMessageBox.warning(self, 'Warning', 'Please select a file to share')
            return

        if not self.dest_ip_input.text():
            QMessageBox.warning(self, 'Warning', 'Please enter the destination IP address')
            return

        self.dest_ip = self.dest_ip_input.text()

        self.connected = True
        self.status_label.setText('Connected to {}'.format(self.dest_ip))

        threading.Thread(target=self.send_file).start()

    def send_file(self):
        try:
            with open(self.file_path, 'rb') as file:
                data = file.read()

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.dest_ip, 4000))
            sock.sendall(data)
            sock.close()

            self.connected = False
            self.status_label.setText('Not connected')
            QMessageBox.information(self, 'Information', 'File sent successfully')

        except Exception as e:
            self.connected = False
            self.status_label.setText('Not connected')
            QMessageBox.warning(self, 'Warning', 'Failed to send file: {}'.format(e))

    def closeEvent(self, event):
        if self.connected:
            QMessageBox.warning(self, 'Warning', 'Please disconnect before closing the window')
            event.ignore()
        else:
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AudioShareWindow()
    window.show()
    sys.exit(app.exec_())
