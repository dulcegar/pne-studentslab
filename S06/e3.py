from seq import Seq
def generate_seqs(pattern, number):
    seq_list = []
    for i in range(1, number +1): #asi excluye el ult numero
        s = Seq(pattern * i) #coges un str y lo mult. por un valor (ej: AC * 1 = AC, luego AC * 2 = ACAC y asi tdo el rato)
        seq_list.append(s)  #añadimos a la lista vacia el objeto que hemos creado
    return seq_list

def print_seqs(seq_list):
    for i, s in enumerate(seq_list):   #enumerate crea una lista nueva y la enumera empezando por 0
        print(f"Sequence {i}: (Length: {s.len()}) {s}")


seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)

print("List 1:")
print_seqs(seq_list1)

print()
print("List 2:")
print_seqs(seq_list2)
