#en este ejercicio modificamos en seq1 el len
from Seq1 import Seq

PRACTICE = 1
EXERCISE = 4
print(F"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

seq_list = [Seq(), Seq("ACTGA"), Seq("Invalid sequence")]
for i, s in enumerate(seq_list):
    print(f"Sequence {i + 1}: (Length: {s.len()}) {s}") #ponemos +1 para q nos empiece por el 1