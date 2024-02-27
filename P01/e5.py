#en este nos pide algo nuevo, crear un count_base()
from Seq1 import Seq

PRACTICE = 1
EXERCISE = 5
print(F"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

seq_list = [Seq(), Seq("ACTGA"), Seq("Invalid sequence")]
for i, s in enumerate(seq_list):
    print(f"Sequence {i + 1}: (Length: {s.len()}) {s}")
    for b in Seq.bases:
        print(f"\t{b}: {s.count_base(b)}") #\t es para tabular