import socket
import threading
from time import sleep

PEERS = [
    ('172.20.10.10', 5000),
    ('172.20.10.7', 5001),
]

def get_my_address():
    my_hostname = socket.gethostname()
    my_ip = socket.gethostbyname(my_hostname)
    
    for peer in PEERS:
        ip, port = peer
        if ip == my_ip:
            return ip, port
            
    raise Exception("My address not found in the PEERS list")

def handle_connection(conn, addr):
    print(f"Connected by {addr}")
    conn.close()

def start_server(my_ip, my_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((my_ip, my_port))
        s.listen(1)
        print(f"Server started on {my_ip}:{my_port}")

        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_connection, args=(conn, addr))
            t.start()

def connect_to_peer(peer):
    ip, port = peer
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            print(f"Connected to {ip}:{port}")
    except Exception as e:
        print(f"Unable to connect to {ip}:{port}")

def main():
    my_ip, my_port = get_my_address()

    # Start the server thread
    server_thread = threading.Thread(target=start_server, args=(my_ip, my_port))
    server_thread.daemon = True
    server_thread.start()

    # Start threads to connect to each peer in the PEERS list, excluding your own IP
    for peer in PEERS:
        ip, _ = peer
        if ip != my_ip:
            t = threading.Thread(target=connect_to_peer, args=(peer,))
            t.start()
            sleep(1)

    # Keep the main thread running
    while True:
        sleep(1)

if __name__ == "__main__":
    main()
