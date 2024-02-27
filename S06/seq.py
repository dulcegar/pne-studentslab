class Seq:
    bases = ["A", "C", "T", "G"]  # nos estamos creando un atributo/propiedad de clase
    '''
    def are_bases_ok(self, strbases):
        ok = True
        for c in strbases:
            if c not in Seq.bases:
                ok = False
                break
        return ok
    '''

    def __init__(self, strbases):

        '''
        for b in strbases:  #recorre la cadena de caracteres de principio a fin
            if b not in Seq.bases:  #como bases es un atributo dentro de la clase, hay q poner el nombre de la clase
                self.strbases = "ERROR!"
                print("Incorrect sequence detected")
                return   #el return corta la ejecucion del constructor
        '''

        # otra forma (usando el break al final en vez de el return)
        # tambien s epodria hacer usando el are_bases_ok
        ok = True
        for b in strbases:  # recorre la cadena de caracteres de principio a fin
            if b not in Seq.bases:  # como bases es un atributo dentro de la clase, hay q poner el nombre de la clase
                ok = False
                self.strbases = "ERROR!"
                print("Incorrect sequence detected")
                break
        if ok:
            self.strbases = strbases
            print("New sequence created!")

    def __str__(self):   #sirve para devolver en una cadena de caracteres la representacion de mi objeto
        return self.strbases   #devolvemos lo que vale el atributo, basicamente el ATGC, en este caso sin adornos

    def len(self):
        return len(self.strbases)  #para que me diga la longitud de la cadena de caracteres


class Gene(Seq):   #indicamos que la clase Gene esta heredando de Seq
    """This class is derived from the Seq Class
       All the objects of class Gene will inherit
       the methods from the Seq class
    """
    def __init__(self, strbases, name=""): #el self siempre va
        super().__init__(strbases) #aqui estan llamando al constructor de la clase padre, y le estamos pasando las bases de la secuencia porq el ya sabe como usarlas
        #siempre que creamos un constructor (init) en la clase hija hay q llamar al init de la clase padre
        self.name = name      #el atributo name es propio de la clase hija
        print("New gene created")

    def __str__(self): #el metodo str sirve para devolver una cadena de caracteres con el estado del objeto
    # no haria falta poner este str porq saldria bien porq hereda el de la clase padre, pero nos piden ponerlo dr una forma en específico: name-bases
        """Print the Gene name along with the sequence"""
        return self.name + "-" + self.strbases   #el self.strbases se hereda


""" #HECHO POR MI de ejemplo
s = Seq("ATGC")
print(s)   #estamos llamando de forma implicita la forma str
print(f"Length of seq: {s.len()}")  #para printear la ongitud de la secuencia
"""
'''
s = Seq("AGTACACTGGT")
g = Gene("CGTAAC", "FRAT1")  #probando la clase hija

print(f"Sequence 1: {s}")
print(f"  Length: {s.len()}")
print(f"Gene: {g}")
'''

