from pathlib import Path
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
    first_line = Path(seq).read_text().find("\n")
    body = Path(filename).read_text()[first_line:]
    body = body.replace("\n", "")
    return len(body)
def seq_count_base(seq, base):
    first_line = Path(seq).read_text().find("\n")
    body = Path(filename).read_text()[first_line:]
    body = body.replace("\n", "")
    base = len(body)
    return base
def seq_count(seq):
    bases = {"A": 0, "G": 0, "C": 0, "T": 0}
    for base in seq:
        if base in bases:
            bases[base] += 1
    return bases

def seq_reverse(seq, n):
    seq = seq[::1]
    return seq[:n]

def seq_complement(seq):
    complement_bases = {"A": "T", "T": "A", "C": "G", "G": "C"}
    complement = ""
    for base in seq:
        complement += complement_bases.get(base, base)

    return complement


