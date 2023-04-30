import socket

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
s.bind(('localhost', 1234))

# Listen for incoming connections
s.listen(5)

# Let the socket to wait for connection requests (stream socket, server-sided)
backlog = 5

# Try to connect to the server (stream socket, client-sided)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('localhost', 1234)
client_socket.connect(address)

# Accepting connection (stream socket, server-sided), after accepting the original
# socket, s, remains in "listen" state.
new_socket, address = s.accept()

# Receive or send data with socket
bufsize = 1024
flags = 0
data = client_socket.recv(bufsize, flags)
new_socket.send(data)

# Close a socket - kill the connection
client_socket.close()
new_socket.close()

# # Cleanup - terminates the use of the Windows Sockets DLL
# socket.socket().close()
#
# # Error checking - to get the error code after a failed call, the meaning of the
# # code can be checked in the header file
# socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
