import os
from Seq1 import Seq

PRACTICE = 1
EXERCISE = 9
print(F"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

s = Seq()
FILENAME = "U5"
if s == "NULL":
    print("NULL Seq created")
else:
    pass




for i, s in enumerate(filename):
    print(f"Sequence {i + 1}: (Length: {s.len()}) {s}")
    print(f"\tBases: {s.count()}")
    print(f"\tRev: {s.reverse()}")
    print(f"\tComp: {s.complement()}")