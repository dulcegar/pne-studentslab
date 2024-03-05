import socket #no solo tiene socket el servidor sinp tbn cada uno de los clientes porq es nuestra forma de comunicacion

# SERVER IP, PORT
# Write here the correct parameter for connecting to the
# Teacher's server
SERVER_PORT = 8081 #NO ES EL PUERTO DEL CLIENTE, es el puerto del servidor, nos conectamos al ip y puerto del servidor
SERVER_IP = "127.0.0.1"  # it depends on the machine the server is running
#ponemos la ip del servidor


# First, create the socket
# We will always use these parameters: AF_INET y SOCK_STREAM
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#estamos creando un socket, es decir un canal de comunicacion en el client socket
#servidor y cliente tienen cad uno su propio socket


# establish the connection to the Server (IP, PORT)
client_socket.connect((SERVER_IP, SERVER_PORT))
# a traves de un cliente me conecto al socket del servidor
#EL CONNECT asocia el socket de nuestro cliente al ip (del servidor) y su propio puerto (nos lo da el sistema operativo, no lo ponemos en ningun lado)
#nos conectamos al ip y al puerto del servidor y a la vez decimos qn es nuestro ip y socket
#el connect tiene relacion directa con el .accept del server.py

# Send data. No strings can be sent, only bytes
# It necesary to encode the string into bytes
client_socket.send(str.encode("HELLO FROM THE CLIENT!!!"))
#send: nos estamos conectando con el recv del server.py
#encode es un metodo estatico de la clase string (porq delante del encode esta el tipo (str))
#encode coge un string y lo convierte en bytes (0 y 1)
#una ves tenemos el mensaje como 0 y 1 se envia al servidor y le llega en forma de bytes

# Close the socket
client_socket.close() #una vez hemos enviado la info. cerramos el canal de comunicacion, cerramos el socket