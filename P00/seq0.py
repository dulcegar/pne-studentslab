from pathlib import Path

BASES = ["A", "C", "T", "G"]
BASES_COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}

def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    first_line = Path(filename).read_text()
    lines = first_line.splitlines()
    body = lines[1:]
    return body
    dna_sequence = ""
    for line in body:
        dna_sequence += line
    return dna_sequence

def seq_len(seq):
    return len(seq)


def seq_count_base(seq, base):
    return seq.count(base)


def seq_count(seq):
    bases_appearances = {}
    for base in BASES:
        bases_appearances[base] = seq_count_base(seq, base)
    return bases_appearances


def seq_reverse(seq, n):
    seq_n = seq[:n]
    return seq_n[::-1]


def seq_complement(seq):
    complement = ""
    for base in seq:
        complement += BASES_COMPLEMENT[base]
    return complement
    # complement = ""
    # for base in seq:
    #     if base == "A":
    #         complement += "T"
    #     elif base == "T":
    #         complement += "A"
    #     elif base == "C":
    #         complement += "G"
    #     elif base == "G":
    #         complement += "C"
    # return complement
