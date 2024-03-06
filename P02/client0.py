import socket

class Client:
    def __init__(self, SERVER_IP: str, SERVER_PORT: int):  #ese ip y ese puerto son del servidor
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT  #nos almacenamos dentro del cliente el ip y el puerto del servidor

    def ping(self):
        print("Ok!")

    def __str__(self): #en el str no hace falta poner mas que self
        return f"Connection to SERVER at {self.SERVER_IP}, PORT: {self.SERVER_PORT}"

    def talk(self, msg):
        import socket #se puede poner tanto arriba como dentro de la funcion
        # -- Create the socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # establish the connection to the Server (IP, PORT)
        client_socket.connect((self.SERVER_IP, self.SERVER_PORT)) #doble parentesis porq es una tupla

        #convertimos en 0 y 1 el mensaje que nos llega
        msg_bytes = str.encode(msg)

        # Send data.
        client_socket.send(msg_bytes)

        # Receive data
        response_bytes = client_socket.recv(2048) #es la capacidad maxima de mi server

        #convertir los bytes en mensaje
        response = response_bytes.decode("utf-8") #no hace falta poner el utf-8 xqe viene por defecto

        # Close the socket
        client_socket.close()

        # Return the response
        return response


c = Client("127.0.0.1", 8081) #ejemplo d crearse un cliente