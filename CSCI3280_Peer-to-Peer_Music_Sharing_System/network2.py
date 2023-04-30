import sys
from PyQt5 import QtWidgets, QtCore, QtGui, QtNetwork


class Client(QtNetwork.QTcpSocket):
    def __init__(self, address, parent=None):
        super().__init__(parent)
        self.address = address
        self.readyRead.connect(self.read_data)

    def read_data(self):
        data = self.readAll().data().decode()
        print(f"Received data from {self.address}: {data}")
        self.disconnectFromHost()


class Server(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.newConnection.connect(self.new_client)

    def new_client(self):
        client_socket = self.nextPendingConnection()
        address = client_socket.peerAddress().toString()
        print(f"New client connected: {address}")
        client = Client(address, client_socket)


class P2PFileSharingSystem(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.port = 5001
        self.server = Server(self)
        self.server.listen(QtNetwork.QHostAddress.Any, self.port)
        print(f"Server listening on port {self.port}")

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("P2P File Sharing System")
        self.setGeometry(100, 100, 400, 200)

        self.address_label = QtWidgets.QLabel(f"Server listening on port {self.port}", self)
        self.address_label.setGeometry(20, 20, 360, 20)

        self.connect_button = QtWidgets.QPushButton("Connect", self)
        self.connect_button.setGeometry(20, 60, 80, 30)
        self.connect_button.clicked.connect(self.connect_to_peer)

        self.file_edit = QtWidgets.QLineEdit(self)
        self.file_edit.setGeometry(20, 100, 250, 30)

        self.browse_button = QtWidgets.QPushButton("Browse", self)
        self.browse_button.setGeometry(280, 100, 80, 30)
        self.browse_button.clicked.connect(self.browse_file)

        self.send_button = QtWidgets.QPushButton("Send", self)
        self.send_button.setGeometry(20, 140, 80, 30)
        self.send_button.clicked.connect(self.send_file)

        self.show()

    def connect_to_peer(self):
        address, ok = QtWidgets.QInputDialog.getText(self, "Connect to Peer", "Enter peer address:")
        if ok:
            client_socket = QtNetwork.QTcpSocket()
            client_socket.readyRead.connect(self.read_data)
            client_socket.connectToHost(address, self.port)

    def browse_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select file")
        self.file_edit.setText(filename)

    def send_file(self):
        filename = self.file_edit.text()
        if filename:
            with open(filename, "rb") as file:
                file_data = file.read()
                for client in self.server.children():
                    if isinstance(client, Client):
                        client.write(file_data)

    def read_data(self):
        client_socket = self.sender()
        data = client_socket.readAll().data().decode()
        print(f"Received data from {client_socket.peerAddress().toString()}: {data}")
        client_socket.disconnectFromHost()

    def closeEvent(self, event):
        self.server.close()
        event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    system = P2PFileSharingSystem()
    sys.exit(app.exec_())
