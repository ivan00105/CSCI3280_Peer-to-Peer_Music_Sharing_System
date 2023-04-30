import requests
import socket

# Function to get the public IP address of the client
def get_public_ip():
    try:
        response = requests.get("http://ipinfo.io/ip")
        return response.text.strip()
    except:
        return None

# Connect to the tracker server and register the client
def register_with_tracker(tracker_ip, tracker_port, client_port):
    tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker_socket.connect((tracker_ip, tracker_port))
    tracker_socket.send(f"register {client_port}".encode())
    tracker_socket.close()

public_ip = get_public_ip()
if public_ip:
    print(f"Public IP: {public_ip}")
    register_with_tracker("137.189.241.64", 1234, 12345)  # Replace TRACKER_IP with the tracker server's IP address
else:
    print("Could not get public IP")
