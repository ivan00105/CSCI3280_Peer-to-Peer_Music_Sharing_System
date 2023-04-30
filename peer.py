import socket
import threading

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
            sock.connect((self.tracker_host, self.tracker_port))
            sock.sendall("GET_PEERS".encode())
            response = sock.recv(1024).decode()
            self.peers = set(response.split(','))
            print(f"Peers: {self.peers}")

    # Other methods like connect_to_peer, start_server, etc. go here
    # ...

port = 12345
tracker_host = "tracker_ip_address"  # Replace with the IP address of the machine running the tracker
tracker_port = 50000
peer = Peer(port, tracker_host, tracker_port)

peer.register_with_tracker()

server_thread = threading.Thread(target=peer.start_server)
server_thread.start()

while True:
    peer.get_peers_from_tracker()
