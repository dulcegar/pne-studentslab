import random
import socket


class NumberGuesser:
    MIN = 1
    MAX = 100

    def __init__(self):
        self.secret_number = random.randint(NumberGuesser.MIN, NumberGuesser.MAX)
        self.attemps = []
        self.guessed = False

    def __str__(self):
        return f"Secret number: {self.secret_number} - Attemps: {self.attemps}"

    def guess(self, number):
        self.attemps.append(number)
        if number < self.secret_number:
            return "Higher"
        elif number > self.secret_number:
            return "Lower"
        else:
            self.guessed = True
            return f"You won after {len(self.attemps)} attemps"

    def is_guessed(self):
        return self.guessed


IP = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server_socket.bind((IP, PORT))
    server_socket.listen()

    print("'Guess the number' server configured!")

    while True:
        print(f"Waiting for connections at ({IP}:{PORT})...")
        (client_socket, client_address) = server_socket.accept()

        nu = NumberGuesser()
        guessed = False
        while not guessed:
            request_bytes = client_socket.recv(2048)
            request = request_bytes.decode()
            n = int(request)

            response = nu.guess(n)
            response_bytes = response.encode()
            client_socket.send(response_bytes)

            print(nu)
            if nu.is_guessed():
                guessed = True
        client_socket.close()
except socket.error as e:
    print(f"Communication error: {e}")
except KeyboardInterrupt:
    print("Server stopped by the admin")
    server_socket.close()
