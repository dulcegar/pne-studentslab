import socket
import termcolor

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

guessed = False
while not guessed:
    try:
        n = int(input("Enter a number: "))
        request = str(n)
        request_bytes = request.encode()
        client_socket.send(request_bytes)

        response_bytes = client_socket.recv(2048)
        response = response_bytes.decode()
        if response == "Lower" or response == "Higher":
            termcolor.cprint(response, "yellow")
        else:
            termcolor.cprint(response, "green")
            guessed = True
    except ValueError:
        print("Please enter a number")
client_socket.close()