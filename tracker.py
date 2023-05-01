import socket
import time

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
    except Exception as e:
        print(f"Error: {e}")
        ip = "Unknown"
    return ip

local_ip = get_local_ip()
print(f"Local IP Address: {local_ip}")

class Tracker:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = set()
        self.disconnected_peers = set()
        self.peer_timestamps = {}

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)

            while True:
                try:
                    client_socket, client_addr = server_socket.accept()
                    data = client_socket.recv(1024).decode()
                    command, *args = data.split()

                    if command == "REGISTER":
                        if args:
                            peer_addr = args[0]

                            # Remove from disconnected_peers if it was previously disconnected
                            if peer_addr in self.disconnected_peers:
                                self.disconnected_peers.discard(peer_addr)

                            self.peers.add(peer_addr)
                            self.peer_timestamps[peer_addr] = time.time()
                            response = "OK"
                        else:
                            response = "INVALID_ARGUMENTS"
                    elif command == "GET_PEERS":
                        # Remove peers that have timed out (e.g., 2 minutes)
                        current_time = time.time()
                        timed_out_peers = {peer for peer in self.peers if current_time - self.peer_timestamps[peer] >= 120}

                        # Update the peers and disconnected_peers sets
                        self.peers -= timed_out_peers
                        self.disconnected_peers |= timed_out_peers

                        # Clear the timestamps for disconnected peers
                        for peer in timed_out_peers:
                            self.peer_timestamps.pop(peer, None)

                        connected_peers = ','.join(self.peers) if self.peers else ''
                        disconnected_peers = ','.join(self.disconnected_peers) if self.disconnected_peers else ''
                        response = f"{connected_peers}|{disconnected_peers}"
                    else:
                        response = "INVALID_COMMAND"

                    client_socket.sendall(response.encode())
                except ConnectionResetError as e:
                    print(f"Error: {e} - Connection was reset by the remote host")
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    client_socket.close()


tracker = Tracker("0.0.0.0", 50000)
tracker.start()
