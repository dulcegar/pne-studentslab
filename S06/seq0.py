from pathlib import Path
def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    first_line = Path(filename).read_text().find("\n")  #quitar la primera linea
    body = Path(filename).read_text()[first_line:]
    body = body.replace("\n", "")
    return body

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
    new_seq = ""
    for c in range(n):
        new_seq = seq[c] + new_seq
    return new_seq

def seq_complement(seq):
    complement_bases = {"A": "T", "T": "A", "C": "G", "G": "C"}
    complement = ""
    for base in seq:
        complement += complement_bases.get(base, base)

    return complement



