from client0 import Client

PRACTICE = 2
EXERCISE = 2

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

# -- Parameters of the server to talk to
IP = "212.128.255.97" # your IP address
PORT = 8081

# -- Create a client object
c = Client(IP, PORT)

print(c)  #este print es para pintar lo que hemos hecho en el def str