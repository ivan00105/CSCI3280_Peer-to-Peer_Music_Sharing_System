import socket
import threading

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

local_ip =  get_local_ip()
print("Your local IP address is:", local_ip)
# List of peers (IP, port) - add more IPs as needed
PEERS = [
    (local_ip, 5000),
    (local_ip, 5001),
]

class SimpleP2P:
    def __init__(self, ip, port, peers):
        self.ip = ip
        self.port = port
        self.peers = peers
        self.connections = []

        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.daemon = True
        self.server_thread.start()

        self.connect_to_peers()

    def run_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.ip, self.port))
        server_socket.listen(5)

        print(f"Server running on {self.ip}:{self.port}")

        while True:
            conn, addr = server_socket.accept()
            self.connections.append(conn)
            print(f"Connected to {addr}")

    def connect_to_peers(self):
        for peer in self.peers:
            if peer != (self.ip, self.port):
                try:
                    peer_ip, peer_port = peer
                    conn = socket.create_connection((peer_ip, peer_port))
                    self.connections.append(conn)
                    print(f"Connected to {peer_ip}:{peer_port}")
                except:
                    print(f"Failed to connect to {peer_ip}:{peer_port}")

def main():

    p2p = SimpleP2P(local_ip, 5000, PEERS)

    # Keep the program running
    while True:
        pass

if __name__ == "__main__":
    main()
