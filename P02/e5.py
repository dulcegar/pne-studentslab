from client0 import Client
from seq import Seq
import os


PRACTICE = 2
EXERCISE = 5
GENE = "FRAT1"
NUMBER_OF_FRAGMENTS = 5
NUMBER_OF_BASES = 10

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.1.129"
PORT = 8081

c = Client(IP, PORT)
print(c)

filename = os.path.join("..", "sequences", GENE + ".txt")
try:
    s = Seq()
    s.read_fasta(filename)
    print(f"Gene {GENE}: {s}")

    for i in range(1, NUMBER_OF_FRAGMENTS + 1):
        print(f"Fragment {i}: ")
except FileNotFoundError:
    print(f"[ERROR]: file '{filename}' not found")