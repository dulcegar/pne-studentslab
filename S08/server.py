import socket #modulo

# Configure the Server's IP and PORT
PORT = 8081
IP = "127.0.0.1"  # it depends on the machine the server is running
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
        #necesitamos mandar un cliente (lo creamos --> client_1.py)

        #a partir de aqui saltamos constantemente de servidor a cliente
        #address en la direccion del cliente, dsd dnd se conecta (IP_client, PORT_client) address es una dupla de la ip y el puerto, el address seria el cartel den nombre del tunel
        #el clientsocket es el canal de comunicacion entero del cliente, el clientsocket seria la autovia por donde se envia la info del servidor al cliente

        # Another connection!e
        number_con += 1  #incrementa en una unidad el number of connections porq se acaba de conectar un cliente

        # Print the connection number
        print(f"CONNECTION: {number_con}. From the address (IP and PORT): {address}")

        # Read the message from the client, if any
        msg = clientsocket.recv(2048).decode("utf-8")  #a traves del canal de comunicacion con el cliente, recibir como maximo 2048 bytes
            #recv (receive) es una accion bloqueante al igual que accept
            #RECEIVE TIENE VINCULACION CON SENT, al igual que accept con connect
            #una vez llega el mensaje en forma de bytes (tras el .send del client_1.py) receive me devuelve bytes pero decode lo transforma en 0 y 1 a string
            #decode: decodifica, transforma los 0 y 1 a string
            #el utf-8 es un formato de string en el q se tiene que decodificar
        print(f"Message from client: {msg}") #pintamos el servidor en su terminal el mensaje del client

        # Send the message, esto tiene efecto en el client-2.py porq en el client-1 no lo tenemos programado lo de recibir un mensaje
        message = "Hello from the teacher's server\n"
        message_bytes = str.encode(message) #transformar el mensaje en bytes
        # We must write bytes, not a string
        clientsocket.send(message_bytes)  #mandamos el mensaje una vez en bytes al client-2
        clientsocket.close() #se cierra la conexion cn el cliente, por cada cliente se abre y se cierra
except socket.error:
    print(f"Problems using ip {IP} port {PORT}. Is the IP correct? Do you have port permission")
except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()