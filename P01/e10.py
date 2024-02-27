from Seq1 import Seq
import os

PRACTICE = 1
EXERCISE = 10
print(F"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

Genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

for gene in Genes:
    filename = os.path.join("..", "sequences", gene)
    try:
        s = Seq()
        s.read_fasta(filename) #initialize the null seq with the given file in fasta format
        print(f"Gene {gene}: Most frequent Base: {s.max_base()}")

    except FileNotFoundError:
        print(f"[ERROR]: file '{filename}' not found")
