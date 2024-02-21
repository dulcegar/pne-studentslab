class Seq:

    def __init__(self, strbases):
        bases = ["A", "C", "T", "G"]
        for b in strbases:
            if b not in bases:
                self.strbases = "ERROR!"
                print("Incorrect sequence detected")
                return

        self.strbases = strbases
        print("New sequence created!")

    def __str__(self):   #sirve para devolver en una cadena de caracteres la representacion de mi objeto
        return self.strbases   #devolvemos lo que vale el atributo, basicamente el ATGC, en este caso sin adornos

    def print_seqs(seq_list):


s1 = Seq("ACCTGC")
s2 = Seq("Hello? Am I a valid sequence?")
print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")

