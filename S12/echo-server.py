import socket
import termcolor

IP = "127.0.0.1"
PORT = 8080


def process_client(client_socket):
    request_bytes = client_socket.recv(2048)
    request = request_bytes.decode()

    print("Message FROM CLIENT: ")
    termcolor.cprint(request, 'green')


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

print("Echo Server configured!")

try:
    while True:
        print("Waiting for clients....")

        (client_socket, client_address) = server_socket.accept()
        process_client(client_socket)
        client_socket.close()
except KeyboardInterrupt:
    print("Server Stopped!")
    server_socket.close()