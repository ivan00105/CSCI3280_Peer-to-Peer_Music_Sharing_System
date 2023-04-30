import socket

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

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)

            while True:
                client_socket, client_addr = server_socket.accept()
                data = client_socket.recv(1024).decode()
                if data == "REGISTER":
                    self.peers.add(client_addr)
                    response = "OK"
                elif data == "GET_PEERS":
                    response = ','.join([f"{addr[0]}:{addr[1]}" for addr in self.peers])
                else:
                    response = "INVALID_COMMAND"

                client_socket.sendall(response.encode())
                client_socket.close()

tracker = Tracker("0.0.0.0", 50000)
tracker.start()
