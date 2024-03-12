def are_bases_ok(strbases):
    ok = True
    for c in strbases:
        if c not in Seq.BASES:
            ok = False
            break
    return ok


class Seq:
    """A class for representing sequences"""
    BASES = ['A', 'T', 'C', 'G']
    COMPLEMENTS = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    def __init__(self, strbases=None):
        if strbases is None or len(strbases) == 0:
            self.strbases = "NULL"
            print("NULL sequence created")
        elif are_bases_ok(strbases):
            self.strbases = strbases
            print("New sequence created!")
        else:
            self.strbases = "ERROR"
            print("INCORRECT Sequence detected")

    def __str__(self):
        return self.strbases

    def len(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return 0
        return len(self.strbases)

    def count_base(self, base):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return 0
        return self.strbases.count(base)

    def count(self):
        bases_appearances = {}
        for base in Seq.BASES:
            bases_appearances[base] = self.count_base(base)  #de count llamamos a count_base
        return bases_appearances

    def reverse(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return self.strbases
        return self.strbases[::-1]

    def complement(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return self.strbases
        result = ""
        for base in self.strbases:
            result += Seq.COMPLEMENTS[base]
        return result

    def read_fasta(self, filename):
        from pathlib import Path

        file_content = Path(filename).read_text()
        lines = file_content.splitlines()
        self.strbases = ""
        for line in lines[1:]:
            self.strbases += line

    def most_frequent_base(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return None
        max_base = ""
        max_count = 0
        for base in Seq.BASES:
            count = self.count_base(base)
            if count > max_count:
                max_count = count
                max_base = base
        return max_base

    def info(self):
        s = f"Sequence: {self.strbases}\n"
        s += f"Total length: {self.len()}\n" #el += es xqe se le suma algo a la 1 linea
        for base, count in self.count().items(): #el count m devuelve un diccionario
            if self.len() == 0: #como no se puede dividir entre 0 xqe nos da error, peta el servidor, hay q arreglar ese error
                percentage = 0
            else:
                percentage = (count * 100) / self.len()
            s += f"{base}: {count} ({percentage:.1f} %)\n"  #la base seria la A y en count el 3, el :.1f es para q tenga 1 solo decimal
        return s




class Gene(Seq):
    """This class is derived from the Seq Class
           All the objects of class Gene will inherit
           the methods from the Seq class
        """
    def __init__(self, strbases, name=""):
        super().__init__(strbases)
        self.name = name
        print("New gene created")

    def __str__(self):
        """Print the Gene name along with the sequence"""
        return self.name + "-" + self.strbases

    def name_len(self):
        return len(self.name)