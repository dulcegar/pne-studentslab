import os
from seq0 import *

GENE = "U5"
N = 20

filename = os.path.join("..", "sequences", GENE)
try:
    dna_sequence = seq_read_fasta(filename)
    fragment = dna_sequence[:N]
    print(f"Gene {GENE}")
    print(f"Fragment: {fragment}")
    print(f"Reverse: {seq_reverse(dna_sequence, N)}")
except FileNotFoundError:
    print(f"[ERROR]: file '{filename}' not found")
except IndexError:
    print(f"[ERROR]: DNA sequence has not almost {N} bases")