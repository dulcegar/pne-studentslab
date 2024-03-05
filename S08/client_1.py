import socket #no solo tiene socket el servidor sinp tbn cada uno de los clientes porq es nuestra forma de comunicacion

# SERVER IP, PORT
# Write here the correct parameter for connecting to the
# Teacher's server
SERVER_PORT = 8081 #NO ES EL PUERTO DEL CLIENTE, es el puerto del servidor, nos conectamos al ip y puerto del servidor
SERVER_IP = ""  # it depends on the machine the server is running


# First, create the socket
# We will always use these parameters: AF_INET y SOCK_STREAM
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#estamos creando un socket, es decir un canal de comunicacion en el client socket
#servidor y cliente tienen cad uno su propio socket


# establish the connection to the Server (IP, PORT)
client_socket.connect((SERVER_IP, SERVER_PORT))
# atraves de un cliente me conecto al socket del servidor
#EL CONNECT asocia el socket de nuestro cliente al ip (del servidor) y su propio puerto (nos lo da el sistema operativo, no lo ponemos en ningun lado)


# Send data. No strings can be sent, only bytes
# It necesary to encode the string into bytes
client_socket.send(str.encode("HELLO FROM THE CLIENT!!!"))

# Close the socket
s.close()