from pythonp2p import Node

class MyNode(Node):
    def on_message(self, message, sender, private):
        print(f"Message from {sender}: {message}")

my_node = MyNode("", 65432, 65433)
my_node.start()

# Connect to another node
my_node.connect_to("IP_ADDRESS", PORT)

# Send a message to all nodes
my_node.send_message("Hello, everyone!")

# Share a file
my_node.setfiledir("downloads")
file_hash = my_node.addfile("path/to/your/file.ext")

# Request a file
my_node.requestFile("FILE_HASH")
