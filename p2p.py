"""
pip install pythonp2p pycryptodome
Rename the folder in site-packages from crypto to Crypto.
"""
from pythonp2p import Node  
import socket
import requests

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

# Function to get the public IP address of the client
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        return response.text.strip()
    except:
        return None


public_ip = get_public_ip()
local_ip =  get_local_ip()
print("Your local IP address is:", local_ip)
print("Your public IP address is :", public_ip)
class MyNode(Node):
    def on_message(self, message, sender, private):
        print(f"Message from {sender}: {message}")

my_node = MyNode("10.0.207.10", 65432, 65433)
my_node.start()

# Connect to another node
# my_node.connect_to("IP_ADDRESS", 65434)

# # Send a message to all nodes
# my_node.send_message("Hello, everyone!")

# # Share a file
# my_node.setfiledir("downloads")
# file_hash = my_node.addfile("path/to/your/file.ext")

# # Request a file
# my_node.requestFile("FILE_HASH")
