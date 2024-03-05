import socket #modulo

# Configure the Server's IP and PORT
PORT = 8081
IP = ""  # it depends on the machine the server is running
MAX_OPEN_REQUESTS = 5 #numero maximo de clientes a los que el servidor va a escuchar a la vez. Deetermina el numero maximo de clientes que va a estar conectados a la vez a mi servidor

# Counting the number of connections (numero de conexiones al servidor)
number_con = 0  #se considera variable

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.socket es porq dentro del modulo (socket.py) hay dentro una clase que se llama socket tbn
#un socket es el mecanismo mas rudimentario de programacion que permite a un proceso comunicarse a traves de la red.
#nos estamos creando un socket, es decir un canal de comunicacion
#el socket.AF_INET, es una propiedad o atributo de clase que esta dentro de clase, sirve para determinar que nuestro socket va a trabajar sobre el protocolo IP
# el socket.SOCK_STREAM es porq nos vamos a mandar y recibir bytes (0 y 1)
try:
    serversocket.bind((IP, PORT))
    #BIND: le estamos diciendo a nuestro server socket que se ate a la dupla montada por el IP y el PORT. Vinculo a un tunel el IP y el puerto
    # become a server socket
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(MAX_OPEN_REQUESTS)
    #LISTEN: hace que se pueda entrar y salir del "tunel", es decir que se puedan conectar clientes a mi servidor
    #es un canal de comunicacion bidimensional, puedo leer y escribir info. es decir, meter y sacar informacion


    while True:
        # accept connections from outside
        print(f"Waiting for connections at {IP}, {PORT} ")
        (clientsocket, address) = serversocket.accept()
        #serversocket.accept --> el accept permote al socket aceptar un cliente
        #el accept es una instruccion bloqueante y hasta q no se desbloquee no se sigue ejecutando
        #ahora mismo nuestro servidor esta parao esperando la conexion de un cliente, sin dar numeros al (clientsocket, address)
        #necesitamos mandar un cliente para dar

        # Another connection!e
        number_con += 1

        # Print the connection number
        print("CONNECTION: {}. From the IP: {}".format(number_con, address))

        # Read the message from the client, if any
        msg = clientsocket.recv(2048).decode("utf-8")
        print("Message from client: {}".format(msg))

        # Send the message
        message = "Hello from the teacher's server\n"
        send_bytes = str.encode(message)
        # We must write bytes, not a string
        clientsocket.send(send_bytes)
        clientsocket.close()
except socket.error:
    print("Problems using ip {} port {}. Is the IP correct? Do you have port permission?".format(IP, PORT))
except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()