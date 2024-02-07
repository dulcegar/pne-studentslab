from pathlib import Path
def seq_ping():
    print("OK")

def seq_read_fasta(filename):
    first_line = Path(filename).read_text().find("\n")  #quitar la primera linea
    body = Path(filename).read_text()[first_line:]
    body = body.replace("\n", "")
    return body

def seq_len(seq):
