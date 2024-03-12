import socket
import os
import termcolor
from seq import Seq

IP = "192.168.0.33"
PORT = 8080
SEQUENCES = ["AACCGTA", "AAA", "TGAT", "CCGGA", "GGGG"]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #para por si esta un port ocupado o ha sido ocupado antes, que no de problema (es opcional)
try:
    server_socket.bind((IP, PORT))
    server_socket.listen()

    print("SEQ Server configured!")

    while True:
        print(f"Waiting for connections at ({IP}:{PORT})...")
        (client_socket, client_address) = server_socket.accept()

        request_bytes = client_socket.recv(2048)
        request = request_bytes.decode()  #transformando los bytes en una cadena de caracteres

        lines = request.splitlines()  #crea una lista y cada linea es uno ["INFO AACCGTA"]
        slices = lines[0].split(' ') #la posicion 0 de esa lista (la primera) es la q nos intersa, y va a separar las dos palabras ["INFO", "AACCGTA"]
        command = slices[0]  #llamamos command a el primer objeto de la lista "slices"
        termcolor.cprint(command, 'green')
        if command == "PING":
            response = "OK!\n"
        elif command == "GET":
            n = int(slices[1])
            bases = SEQUENCES[n]
            s = Seq(bases)
            response = str(s)
        elif command == "INFO":
            bases = slices[1]  #la posicion 0 es el comando y en la 1 estarian las bases
            s = Seq(bases)
            response = s.info() #el info ya lo teniamos creado en Seq.py
        elif command == "COMP":
            bases = slices[1]
            s = Seq(bases)
            response = s.complement()  #el complement ya lo teniamos creado en Seq.py
        elif command == "REV":
            bases = slices[1]
            s = Seq(bases)
            response = s.reverse()
        elif command == "GENE":
            gene = slices[1] #nombre del gen
            s = Seq() #me creo la secuencia nula
            filename = os.path.join("..", "sequences", gene) #me meto en la carpeta
            s.read_fasta(filename)
            response = str(s)

        print(response)
        response_bytes = response.encode()
        client_socket.send(response_bytes)

        client_socket.close()
except socket.error:
    print(f"Problems using port {PORT}. Do you have permission?")
except KeyboardInterrupt:
    print("Server stopped by the admin")
    server_socket.close()