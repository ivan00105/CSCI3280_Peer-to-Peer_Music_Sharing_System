import socket
import threading

TRACKER_IP = "0.0.0.0"  # Use "0.0.0.0" to listen on all available network interfaces
TRACKER_PORT = 1234

# Dictionary to store registered clients (key: IP and port, value: timestamp)
registered_clients = {}


def handle_client(client_socket, client_address):
    global registered_clients

    data = client_socket.recv(1024).decode().split()
    if data[0] == "register":
        client_port = int(data[1])
        registered_clients[(client_address[0], client_port)] = time.time()
        print(f"Registered client: {client_address[0]}:{client_port}")


def start_tracker_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((TRACKER_IP, TRACKER_PORT))
    server_socket.listen(5)
    print(f"Tracker server is listening on {TRACKER_IP}:{TRACKER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    start_tracker_server()
