from Seq1 import Seq
PRACTICE = 1
EXERCISE = 9
print(F"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

GENES = ["U5", "ADA", "FRAT1", "FXN"]
for gene in GENES:
    filename = os.path.join("..", "sequences", gene)   #no pongo ' + ".txt"' porq no los tengo guardados asi en mi carpeta
    try:
        dna_sequence = seq_read_fasta(filename)
        print(f"Gene {gene} -> Length: {seq_len(dna_sequence)}")
    except FileNotFoundError:
        print(f"[ERROR]: file '{filename}' not found")

seq_list = [Seq(), Seq("ACTGA"), Seq("Invalid sequence")]
for i, s in enumerate(seq_list):
    print(f"Sequence {i + 1}: (Length: {s.len()}) {s}")
    print(f"\tBases: {s.count()}")
    print(f"\tRev: {s.reverse()}")
    print(f"\tComp: {s.complement()}")