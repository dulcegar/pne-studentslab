from Seq1 import Seq
import os

PRACTICE = 1
EXERCISE = 9
print(F"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

s = Seq()
Gene = "U5"
filename = os.path.join("..", "sequences", Gene)
try:
    s.read_fasta(filename)
    print(f"Sequence: (Length: {s.len()}) {s}\nBases: {s.count()}\nRev: {s.reverse()}\nComp: {s.complement()}")

except FileNotFoundError:
    print(f"[ERROR]: file '{filename}' not found")

