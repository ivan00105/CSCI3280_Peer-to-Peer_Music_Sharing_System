import os
import threading
from pythonp2p import Node
import socket
import requests
import json

class InterleavingNode(Node):
    def request_chunk(self, node_ip, image_index, image_name, chunk_index):
        data = {
            "action": "request_chunk",
            "image_index": image_index,
            "image_name": image_name,
            "chunk_index": chunk_index,
        }
        for node in self.nodes_connected:
            if node.host == node_ip:
                node.send(json.dumps(data))

    def on_message(self, data, sender, private):
        super().on_message(data, sender, private)
        parsed_data = json.loads(data)
        if parsed_data["action"] == "send_chunk":
            image_index = parsed_data["image_index"]
            image_name = parsed_data["image_name"]
            chunk = parsed_data["chunk"]
            print(f"Received chunk from {sender} for image {image_name}: {chunk}")
        elif parsed_data["action"] == "request_chunk":
            image_index = parsed_data["image_index"]
            image_name = parsed_data["image_name"]
            chunk_index = parsed_data["chunk_index"]
            chunk = self.read_image_chunk(image_name, chunk_index)
            data = {
                "action": "send_chunk",
                "image_index": image_index,
                "image_name": image_name,
                "chunk": chunk,
            }
            self.send_message(json.dumps(data), sender)

    @staticmethod
    def read_image_chunk(image_name, chunk_index, chunk_size=1024):
        with open(image_name, "rb") as f:
            f.seek(chunk_index * chunk_size)
            chunk = f.read(chunk_size)
        return chunk.decode("ISO-8859-1")  # Use ISO-8859-1 encoding to handle binary data


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

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        return response.text.strip()
    except:
        return None

def get_connected_nodes_ip_addresses(node):
    return [n.host for n in node.nodes_connected]

def interleave_images(node, image_names, chunk_size=1024):
    connected_nodes_ips = get_connected_nodes_ip_addresses(node)
    used_images = image_names[:len(connected_nodes_ips)]

    for i, image_name in enumerate(used_images):
        node_ip = connected_nodes_ips[i % len(connected_nodes_ips)]
        node.request_chunk(node_ip, i, image_name)


public_ip = get_public_ip()
local_ip = get_local_ip()
print("Your local IP address is:", local_ip)
print("Your public IP address is :", public_ip)

my_node = InterleavingNode(local_ip, 65432, 65433)
my_node.start()

image_names = ["1-1.bmp", "1-2.bmp", "1-3.bmp"]
chunk_size = 1024
# Connect to other nodes and share images
# my_node.connect_to("NODE_IP", 65432)

# After connecting to other nodes, call interleave_images to request image chunks
# interleave_images(my_node, image_names, chunk_size)
