import socket
import threading
import time


class Peer:
    def __init__(self, port, tracker_host, tracker_port):
        self.port = port
        self.tracker_host = tracker_host
        self.tracker_port = tracker_port
        self.peers = set()

    def register_with_tracker(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.tracker_host, self.tracker_port))
            sock.sendall("REGISTER".encode())
            response = sock.recv(1024).decode()
            if response == "OK":
                print("Registered with tracker")

    def get_peers_from_tracker(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.tracker_host, self.tracker_port))
                sock.sendall("GET_PEERS".encode())
                response = sock.recv(1024).decode()
                new_peers = set(response.split(','))

                if new_peers != self.peers:
                    self.peers = new_peers
                    print(f"Peers: {self.peers}")
            except Exception as e:
                print(f"Error getting peers from tracker: {e}")

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", self.port))
        server_socket.listen(5)

        while True:
            client_socket, client_addr = server_socket.accept()
            print(f"Connected to {client_addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        # Your logic to handle client connections goes here
        pass


port = 12345
tracker_host = "172.20.10.7"  # Replace with the IP address of the machine running the tracker
tracker_port = 50000
peer = Peer(port, tracker_host, tracker_port)

peer.register_with_tracker()

server_thread = threading.Thread(target=peer.start_server)
server_thread.start()

while True:
    peer.get_peers_from_tracker()
    time.sleep(1)