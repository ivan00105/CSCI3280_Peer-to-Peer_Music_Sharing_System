import socket

HOST = ''    # listen on all available network interfaces
PORT = 12345 # use the same port number as in the sender program

def receive_file():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(1)

        print('Waiting for incoming connection...')
        conn, addr = sock.accept()

        with open('received_file.mp3', 'wb') as file:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                file.write(data)

        print('File received successfully')

    except Exception as e:
        print('Failed to receive file:', e)

    finally:
        conn.close()
        sock.close()

if __name__ == '__main__':
    receive_file()
