from Seq1 import Seq

PRACTICE = 1
EXERCISE = 2
print(F"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

seq_list = [Seq(), Seq("TATAC")]
for i, s in enumerate(seq_list):
    print(f"Sequence {i + 1}: {s}") #ponemos +1 para q nos empiece por el 1


