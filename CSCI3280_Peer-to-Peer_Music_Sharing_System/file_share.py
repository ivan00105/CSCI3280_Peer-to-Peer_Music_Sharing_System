import socket
import threading
import os
import sys
import time
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeWidgetItem, QPushButton, QTreeWidget

# Create the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('File Sharing App')
        self.setGeometry(200, 200, 800, 600)

        self.remote_host = '192.168.10.4'
        self.remote_port = 5000

        # Set up the UI elements
        self.treeWidget = QTreeWidget(self)
        self.treeWidget.setHeaderLabels(['File Name', 'File Size (bytes)', 'Node IP'])
        self.setCentralWidget(self.treeWidget)

        self.browseButton = QPushButton('Browse', self)
        self.browseButton.setGeometry(20, 20, 80, 30)
        self.browseButton.clicked.connect(self.browse_for_file)

        self.shareButton = QPushButton('Share', self)
        self.shareButton.setGeometry(120, 20, 80, 30)
        self.shareButton.clicked.connect(self.share_files)

        self.refreshButton = QPushButton('Refresh', self)
        self.refreshButton.setGeometry(220, 20, 80, 30)
        self.refreshButton.clicked.connect(self.refresh_files)

        self.statusBar().showMessage('Ready')

        # Set up the socket for listening for incoming file transfers
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind(('127.0.0.1', 5000))
        self.listen_socket.listen(5)

        # Set up a thread for handling incoming file transfers
        self.transfer_thread = threading.Thread(target=self.handle_file_transfers)
        self.transfer_thread.start()

        # Set up a thread for broadcasting our available files to other nodes
        self.broadcast_thread = threading.Thread(target=self.broadcast_files)
        self.broadcast_thread.start()

    def refresh_files(self):
        self.treeWidget.clear()
        files = os.listdir('.')
        for filename in files:
            if os.path.isfile(filename):
                size = os.path.getsize(filename)
                item = QTreeWidgetItem([filename, f"{size} bytes"])
                self.treeWidget.addTopLevelItem(item)


    def handle_file_transfers(self):
        while True:
            conn, addr = self.listen_socket.accept()
            file_info = json.loads(conn.recv(1024).decode())
            file_size = int(file_info['size'])
            file_name = file_info['name']
            with open(file_name, 'wb') as f:
                while file_size > 0:
                    data = conn.recv(1024)
                    f.write(data)
                    file_size -= len(data)
            conn.close()

    def broadcast_files(self):
        while True:
            # Scan the local directory for files to share
            files = []
            for filename in os.listdir():
                if os.path.isfile(filename):
                    files.append(filename)
            # Broadcast the available files to other nodes on the network
            for node in self.get_nodes():
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((node, 5000))
                    s.sendall(json.dumps(files).encode())
                    s.close()
                except:
                    pass
            time.sleep(5)

    def get_nodes(self):
        # Returns a list of nodes on the network to share files with
        return ['192.168.100.4', '192.168.10.3']

    def browse_for_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Select file to share')[0]
        if file_name:
            item = QTreeWidgetItem([os.path.basename(file_name), str(os.path.getsize(file_name)), ''])
            self.treeWidget.addTopLevelItem(item)

    def share_files(self):
        # Connect to remote peer
        self.listen_socket.connect((self.remote_host, self.remote_port))

        # Send file name and size to remote peer
        self.listen_socket.sendall(f"{self.file_name}#{self.file_size}".encode('utf-8'))

        # Send file data to remote peer
        with open(self.file_path, 'rb') as f:
            data = f.read(1024)
            while data:
                self.listen_socket.sendall(data)
                data = f.read(1024)

        # Close socket connection
        self.listen_socket.close()

    def handle_file_transfer(self, node_ip, file_name, file_size):
        try:
            # Connect to the remote node
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((node_ip, 5000))

            # Send the file info
            file_info = {'name': file_name, 'size': file_size}
            s.sendall(json.dumps(file_info).encode())

            # Send the file data
            with open(file_name, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    s.sendall(data)
        except:
            pass
        finally:
            s.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
