import socket
import threading
import time
import json
import pickle
from PyQt5.QtCore import QObject, pyqtSignal
from upnp_port_forward import forwardPort
from concurrent.futures import ThreadPoolExecutor

class Peer(QObject):
    song_list_received = pyqtSignal(list)

    def __init__(self, server_port, tracker_host, tracker_port, music_player):
        super().__init__()
        self.server_port = server_port
        self.tracker_host = tracker_host
        self.tracker_port = tracker_port
        self.peers = set()
        self.sent_song_list = {}
        self.music_player = music_player
        self.song_list_received.connect(music_player.update_merged_song_list)

        # Forward the server_port using UPnP
        self.forward_port_using_upnp()

    def forward_port_using_upnp(self):
        eport = self.server_port  # External port
        iport = self.server_port  # Internal port
        router = None  # Specify router IP, if needed
        lanip = None  # Specify LAN IP, if needed
        disable = False  # Set to True if you want to disable the port forwarding
        protocol = 'TCP'  # Protocol to use for forwarding
        time = 0  # Lease duration, 0 for indefinite
        description = 'Music App Port Forwarding'  # Description for the port forwarding entry
        verbose = True  # Set to True for detailed output

        success = forwardPort(eport, iport, router, lanip, disable, protocol, time, description, verbose)
        if success:
            print("Port forwarding successful.")
        else:
            print("Port forwarding failed. Application may not work as expected.")


    def register_with_tracker(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.tracker_host, self.tracker_port))
                local_ip = self.get_local_ip()
                register_message = f"REGISTER {local_ip}:{self.server_port}"
                sock.sendall(register_message.encode())
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
                connected_peers, disconnected_peers = response.split('|')  # Assuming '|' separates the two lists in the response

                new_peers = set(connected_peers.split(',')) if connected_peers else set()
                disconnected_peers = set(disconnected_peers.split(',')) if disconnected_peers else set()
                # Remove disconnected peers
                for peer in disconnected_peers:
                    self.peers.discard(peer)
                    self.sent_song_list.pop(peer, None)
                # Add new peers
                for peer in new_peers:
                    if peer not in self.peers:
                        self.peers.add(peer)
                        self.sent_song_list[peer] = False
                        self.handle_peer(tuple(peer.split(':')))  # Send the song list to the new peer immediately
                print(f"Peers: {self.peers}")
                # Send a heartbeat signal to the tracker
                self.register_with_tracker()
        except TimeoutError:
            print("Failed to connect to the tracker. The application will work in offline mode.")
        except Exception as e:
            print(f"Error getting peers from tracker: {e}")

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("", self.server_port))
        server_socket.listen(5)

        try:
            while True:
                try:
                    client_socket, client_addr = server_socket.accept()
                    threading.Thread(target=self.handle_client, args=(client_socket, client_addr), name="handle_client").start()
                except Exception as e:
                    print(f"Error: {e}")
        finally:
            server_socket.close()

    def handle_client(self, client_socket, client_addr):
        song_list = self.receive_song_list(client_socket)  # Change client_addr to client_socket
        if song_list is not None:
            print(f"Received song list: {song_list}")
            self.song_list_received.emit(song_list)

    def should_send_song_list(self, peer_addr):
        if peer_addr not in self.sent_song_list:
            self.sent_song_list[peer_addr] = False
        return not self.sent_song_list[peer_addr]
    def is_peer_connected(self, peer_addr):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)  # Set a short timeout for the connection
                sock.connect(peer_addr)
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

    def start_client(self):
        self.sent_song_list = {}
        thread_pool = ThreadPoolExecutor(max_workers=10)  # Adjust the number of workers as needed

        while True:
            self.get_peers_from_tracker()

            for peer in list(self.peers):
                peer_addr = tuple(peer.split(':'))
                peer_addr = (peer_addr[0], int(peer_addr[1]))

                if not self.is_peer_connected(peer_addr):
                    self.peers.remove(peer)
                    self.sent_song_list.pop(peer, None)
                else:
                    thread_pool.submit(self.handle_peer, peer_addr)

            time.sleep(1)  # Add a delay between each iteration


    def update_received_song_list(self, received_song_list):
        self.received_song_list = received_song_list
        self.select_songs(self.current_search_text)
        
    def send_song_list(self, song_list, peer_addr):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                host, port = peer_addr
                sock.settimeout(5)  # Set a timeout for the socket connection
                sock.connect((host, port))
                sock.sendall(json.dumps(song_list).encode())
                print("song list sent")
            except Exception as e:
                print(f"Error sending song list: {e}")


    def receive_song_list(self, client_socket):  # Change client_addr to client_socket
        try:
            data = client_socket.recv(4096)  # Remove this line
            song_list = json.loads(data.decode())
            return song_list
        except Exception as e:
            print(f"Error getting songs from client_socket {client_socket}: {e}")
            return None

    def handle_peer(self, peer_addr):
        if self.should_send_song_list(peer_addr):
            self.send_song_list(self.music_player.song_path_list, peer_addr)
            self.sent_song_list[peer_addr] = True




    def get_local_ip(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
        except Exception as e:
            print(f"Error: {e}")
            ip = "Unknown"
        return ip



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