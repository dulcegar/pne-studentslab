import os
from seq0 import *

GENES = ["U5", "ADA", "FRAT1", "FXN"]

for gene in GENES:
    filename = os.path.join("..", "sequences", gene)   #no pongo ' + ".txt"' porq no los tengo guardados asi en mi carpeta
    try:
        dna_sequence = seq_read_fasta(filename)
        print(f"Gene {gene} -> Length: {seq_len(dna_sequence)}")
    except FileNotFoundError:
        print(f"[ERROR]: file '{filename}' not found")