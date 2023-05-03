import socket
import threading

class Peer:
    def __init__(self, port, broadcast_port):
        self.port = port
        self.broadcast_port = broadcast_port
        self.peers = set()

    # Discover peers, connect to peers, and handle incoming connections methods go here
    def discover_peers(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            message = f"{socket.gethostbyname(socket.gethostname())}:{self.port}"
            sock.sendto(message.encode(), ('255.255.255.255', self.broadcast_port))

    def listen_broadcasts(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(("", self.broadcast_port))

            while True:
                data, addr = sock.recvfrom(1024)
                peer = data.decode()
                if peer != f"{socket.gethostbyname(socket.gethostname())}:{self.port}":
                    self.peers.add(peer)
                print(f"Current peers: {self.peers}")
                
    def connect_to_peer(self, peer_host, peer_port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((peer_host, peer_port))
        # Your logic to communicate with the connected peer goes here

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
broadcast_port = 50000
peer = Peer(port, broadcast_port)

server_thread = threading.Thread(target=peer.start_server)
server_thread.start()

broadcast_listener_thread = threading.Thread(target=peer.listen_broadcasts)
broadcast_listener_thread.start()

while True:
    peer.discover_peers()
