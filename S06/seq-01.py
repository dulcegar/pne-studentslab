class Seq:
    def __init__(self, strbases):
        self.strbases = strbases
        print("New sequence created!")

    def __str__(self):   #sirve para devolver en una cadena de caracteres la representacion de mi objeto
        return self.strbases   #devolvemos lo que vale el atributo, basicamente el ATGC, en este caso sin adornos

    def len(self):
        return len(self.strbases)  #para que me diga la longitud de la cadena de caracteres

""" #HECHO POR MI de ejemplo
s = Seq("ATGC")
print(s)   #estamos llamando de forma implicita la forma str
print(f"Length of seq: {s.len()}")  #para printear la ongitud de la secuencia
"""

s1 = Seq("AGTACACTGGT")
s2 = Seq("CGTAAC")

print(f"Sequence 1: {s1}")
print(f"  Length: {s1.len()}")
print(f"Sequence 2: {s2}")
print(f"  Length: {s2.len()}")

