import socket
import threading
import time
import json
import pickle
from PyQt5.QtCore import QObject, pyqtSignal

class Peer(QObject):
    song_list_received = pyqtSignal(list)

    def __init__(self, server_port, tracker_host, tracker_port, music_player):
        super().__init__()
        self.server_port = server_port
        self.tracker_host = tracker_host
        self.tracker_port = tracker_port
        self.peers = set()
        self.music_player = music_player
        self.song_list_received.connect(music_player.update_merged_song_list)

    def register_with_tracker(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.tracker_host, self.tracker_port))
                sock.sendall("REGISTER".encode())
                response = sock.recv(1024).decode()
                if response == "OK":
                    print("Registered with tracker")
        except TimeoutError:
            print("Failed to connect to the tracker. The application will work in offline mode.")

    def get_peers_from_tracker(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.tracker_host, self.tracker_port))
                sock.sendall("GET_PEERS".encode())
                response = sock.recv(1024).decode()
                new_peers = set(response.split(','))

                if new_peers != self.peers:
                    self.peers = new_peers
                    print(f"Peers: {self.peers}")

                # Send a heartbeat signal to the tracker
                sock.sendall("REGISTER".encode())
        except TimeoutError:
            print("Failed to connect to the tracker. The application will work in offline mode.")
        except Exception as e:
            print(f"Error getting peers from tracker: {e}")

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("", self.server_port))
        server_socket.listen(5)

        while True:
            client_socket, client_addr = server_socket.accept()
            print(f"Connected to {client_addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            time.sleep(1)

    def handle_client(self, client_socket):
        peer_addr = client_socket.getpeername()
        song_list = self.receive_song_list(client_socket, peer_addr) 
        if song_list is not None:
            print(f"Received song list: {song_list}")
            self.song_list_received.emit(song_list)

    def update_received_song_list(self, received_song_list):
        self.received_song_list = received_song_list
        self.select_songs(self.current_search_text)
        
    def send_song_list(self, song_list, peer_addr):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                host, port = peer_addr
                sock.settimeout(5)  # Set a timeout for the socket connection
                sock.connect((host, int(port)))
                sock.sendall(json.dumps(song_list).encode())
            except Exception as e:
                print(f"Error sending song list: {e}")

    def receive_song_list(self, client_socket, peer_addr):
        try:
            data = client_socket.recv(4096)
            song_list = json.loads(data.decode())
            return song_list
        except Exception as e:
            print(f"Error getting songs from peer {peer_addr}: {e}")
            return None





# port = 12345
# tracker_host = "172.20.10.7"  # Replace with the IP address of the machine running the tracker
# tracker_port = 50000
# peer = Peer(port, tracker_host, tracker_port)

# peer.register_with_tracker()

# server_thread = threading.Thread(target=peer.start_server)
# server_thread.start()

# while True:
#     peer.get_peers_from_tracker()
#     time.sleep(1)