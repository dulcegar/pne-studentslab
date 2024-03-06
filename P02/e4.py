from client0 import Client
from seq import Seq
import os


PRACTICE = 2
EXERCISE = 4
GENES = ["U5", "FRAT1", "ADA"]

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.0.33"
PORT = 8081


c = Client(IP, PORT)

for gene in GENES: #ponemos el for xqe hay unos cuantos
    filename = os.path.join("..", "sequences", gene) #nos estamos metiendo en la carpeta sequences y en el fichero que queremos
    try:
        s = Seq()
        s.read_fasta(filename) #llenamos la secuencia vacia del filename q acabamos de crear (es decir, el fichero de la carpeta sequences)

        #primer mensaje
        msg = f"Sending {gene} Gene to server..."
        print(f"To Server: {msg}")
        response = c.talk(msg)
        print(f"From server: \n {response}")

        #segundo mensaje
        msg = s.__str__()  # msg = f"{s}"  /  msg = str(s)
        print(f"To Server: {msg}")
        response = c.talk(msg)
        print(f"From server: \n {response}")

    except FileNotFoundError:
        print(f"[ERROR]: file '{filename}' not found")
