from Client0 import Client
from seq import Seq
import os


PRACTICE = 2
EXERCISE = 6
GENE = "FRAT1"
NUMBER_OF_FRAGMENTS = 10
NUMBER_OF_BASES = 10

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.0.30"
PORT1 = 8080
PORT2 = 8081

c1 = Client(IP, PORT1)
print(c1)
c2 = Client(IP, PORT2)
print(c2)

filename = os.path.join("..", "sequences", GENE + ".txt")
try:
    s = Seq()
    s.read_fasta(filename)
    print(f"Gene {GENE}: {s}")

    msg = f"Sending {GENE} Gene to the server, in fragments of {NUMBER_OF_BASES} bases..."
    c1.talk(msg)
    c2.talk(msg)

    start = 0
    end = NUMBER_OF_BASES
    for i in range(1, NUMBER_OF_FRAGMENTS + 1):
        s_str = str(s)
        fragment = s_str[start:end]
        msg = f"Fragment {i}: {fragment}"
        print(msg)
        if i % 2 != 0:
            c1.talk(msg)
        else:
            c2.talk(msg)

        start += NUMBER_OF_BASES
        end += NUMBER_OF_BASES
except FileNotFoundError:
    print(f"[ERROR]: file '{filename}' not found")