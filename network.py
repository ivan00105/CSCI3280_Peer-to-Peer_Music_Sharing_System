import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QTextEdit, QWidget, \
    QInputDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import socket
import threading
import requests # if pip install requests does not work, run "python -m pip install requests"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print("Error getting local IP address:", e)
        return None

# Function to get the public IP address of the client
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        return response.text.strip()
    except:
        return None


public_ip = get_public_ip()
local_ip =  get_local_ip()
print("Your local IP address is:", local_ip)
print("Your public IP address is :", public_ip)

class ServerThread(QThread):
    new_message = pyqtSignal(str)

    def __init__(self, port):
        super(ServerThread, self).__init__()
        self.port = port

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', self.port))
        server_socket.listen(5)
        self.new_message.emit("Server is listening on port {}".format(self.port))
        while True:
            client_socket, client_address = server_socket.accept()
            self.new_message.emit("Connection from {}:{}".format(client_address[0], client_address[1]))
            client_socket.send("Welcome to the chat!".encode())
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                self.new_message.emit("{}:{}: {}".format(client_address[0], client_address[1], data))
                client_socket.send(data.encode())
            client_socket.close()


class ClientThread(QThread):
    new_message = pyqtSignal(str)

    def __init__(self, ip, port):
        super(ClientThread, self).__init__()
        self.ip = ip
        self.port = port

    def run(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.ip, self.port))
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            self.new_message.emit("Server: {}".format(data))
        client_socket.close()


class ChatWindow(QMainWindow):
    def __init__(self):
        super(ChatWindow, self).__init__()

        self.setWindowTitle("TCP Chat")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.vertical_layout = QVBoxLayout()

        self.message_label = QLabel("Received Messages:")
        self.vertical_layout.addWidget(self.message_label)

        self.message_text_edit = QTextEdit()
        self.message_text_edit.setReadOnly(True)
        self.vertical_layout.addWidget(self.message_text_edit)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_server)
        self.vertical_layout.addWidget(self.connect_button)

        self.central_widget.setLayout(self.vertical_layout)

        self.server_thread = None
        self.client_thread = None

    def connect_to_server(self):
        if self.client_thread is not None:
            self.client_thread.terminate()
            self.client_thread = None

        ip, ok = QInputDialog.getText(self, "Connect to Server", "Enter IP address:")
        if ok:
            port, ok = QInputDialog.getInt(self, "Connect to Server", "Enter port number:")
            if ok:
                self.client_thread = ClientThread(ip, port)
                self.client_thread.new_message.connect(self.update_message_text_edit)
                self.client_thread.start()

    def start_server(self, port):
        if self.server_thread is not None:
            self.server_thread.terminate()
            self.server_thread = None

        self.server_thread = ServerThread(port)
        self.server_thread.new_message.connect(self.update_message_text_edit)
        self.server_thread.start()

    def update_message_text_edit(self, message):
        self.message_text_edit.append(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    chat_window = ChatWindow()
    chat_window.show()

    # Start the server on a specific port (you can modify this to your desired port)
    chat_window.start_server(5555)

    sys.exit(app.exec_())



