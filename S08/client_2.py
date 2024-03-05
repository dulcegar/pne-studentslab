import socket

# SERVER IP, PORT
SERVER_PORT = 8081
SERVER_IP = "127.0.0.1"  # it depends on the machine the server is running

# First, create the socket
# We will always use these parameters: AF_INET y SOCK_STREAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# establish the connection to the Server (IP, PORT)
s.connect((SERVER_IP, SERVER_PORT))

# Send data. No strings can be sent, only bytes
# It necesary to encode the string into bytes
s.send(str.encode("HELLO FROM THE CLIENT!!!"))

# Receive data from the server
# esta es la parte distinta que tenemos del client-1
msg = s.recv(2048)  #el cliente aqui se bloquea (por el recv) y entre parentesis el tamaño del buffer
print("MESSAGE FROM THE SERVER:\n")
print(msg.decode("utf-8"))  #decodifica en utf-8 el mensaje en bytes del servidor

# Closing the socket
s.close()