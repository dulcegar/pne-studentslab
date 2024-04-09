import socket
import termcolor
from pathlib import Path
import os

IP = "192.168.0.33"
PORT = 8080

#para comprobar si esta bien hay q poner en google: http://127.0.0.1:8080/info/A
#hay que ir cambiando el ip, el puerto y lo que queramos buscar

def process_client(client_socket):
    request_bytes = client_socket.recv(2048)
    request = request_bytes.decode()   #transformar los butes en una cadena de caracteres
    lines = request.splitlines()  #genera una lista de las lineas del http
    request_line = lines[0]   #estamos almacenando en una variable la posicion 0 de la lista de lineas que acabamos de crear (la 1 linea es de request)
    print("Request line: ", end="")
    termcolor.cprint(request_line, 'green')
    slices = request_line.split(' ')  #divide la cadena de caracteres original en varias cadenas de caracteres
    method = slices[0]   #nos almacenamos el metodo que puede ser el GET, ....
    resource = slices[1] #path=resource, es el recurso que solicita el cliente al servidor
    version = slices[2] #esta en gris xqe no lo usamos

    if resource == "/info/A":  #si la persona escribe /info/A en la 2 posicion
        file_name = os.path.join("html", "A.html") #me crea un string
        body = Path(file_name).read_text() #el Path es una clase que esta dentro del modulo pathlib. Nos estamos creando un objeto de la clase Path, es la llamda al constructor. Llamos al metodo con read_text y me lee tdo el fichero A.html.
        status_line = "HTTP/1.1 200 OK\n"  #es la primera linea de la respuesta del servidor. El 200 es el numero del estado
    elif resource == "/info/C":   #basicamente en cada if/elif genera la ruta al fichero que tiene que abrir
        file_name = os.path.join("html", "C.html")
        body = Path(file_name).read_text()
        status_line = "HTTP/1.1 200 OK\n"
    elif resource == "/info/G":
        file_name = os.path.join("html", "G.html")
        body = Path(file_name).read_text()
        status_line = "HTTP/1.1 200 OK\n"
    elif resource == "/info/T":
        file_name = os.path.join("html", "T.html")
        body = Path(file_name).read_text()
        status_line = "HTTP/1.1 200 OK\n"
    else:  #si entramos por el else es porq el resorce que ha pedido el cliente no existe
        file_name = os.path.join("html", "error.html") #en vez de devolver una pag web en blanco, devoldemos el error
        body = Path(file_name).read_text()
        status_line = "HTTP/1.1 404 Not_found\n" #no hay error asociado pero aparece el mensaje
    header = "Content-Type: text/html\n" #me estoy almacenando en la variable header que el servidor va a contestar con un html. de que tipo es el contenido que envia el servidor
    header += f"Content-Length: {len(body)}\n" #añadimos al header, otra cabecera donde ponemos la longitud del contenido, esto es, cuantos bytes ocupan lo que le va a pasar el servidor
    response = f"{status_line}{header}\n{body}" #variable que representa la respuesta que le envia al cliente, cadena d caracteres con el formato de una respuesta de http
    response_bytes = response.encode()
    client_socket.send(response_bytes)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

print("DNA Bases Server configured!")

try:
    while True:
        print("Waiting for clients...")

        (client_socket, client_address) = server_socket.accept()
        process_client(client_socket)
        client_socket.close()
except KeyboardInterrupt:
    print("Server Stopped!")
    server_socket.close()
