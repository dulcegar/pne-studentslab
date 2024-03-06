from pathlib import Path

class Seq:
    bases = ["A", "C", "T", "G"]
    bases_complement = {"A": "T", "T": "A", "C": "G", "G": "C"}

    def __init__(self, strbases=None):
        if strbases is None or len(strbases) == 0:
            self.strbases = "NULL"
            print ("NULL sequence created")

        else:
            ok = True
            for b in strbases:
                if b not in Seq.bases:
                    ok = False
                    self.strbases = "ERROR"
                    print("Invalid sequence detected")
                    break
            if ok:
                self.strbases = strbases
                print("New sequence created!")

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
        for base in Seq.bases:
            bases_appearances[base] = self.count_base(base) #llamamos a count base
        return bases_appearances

    def reverse(self):
        if self.strbases is "NULL":
            return "NULL"

        elif self.strbases is "ERROR":
            return "ERROR"
        else:
            new_seq = self.strbases[:]
            return new_seq[::-1]

    def complement(self):
        if self.strbases is "NULL":
            return "NULL"

        elif self.strbases is "ERROR":
            return "ERROR"
        else:
            complement = ""
            for base in self.strbases:
                complement += Seq.bases_complement[base]
            return complement

    def read_fasta(self, filename):
        first_line = Path(filename).read_text()
        lines = first_line.splitlines()
        body = lines[1:]

        dna_sequence = ""
        for line in body:
            dna_sequence += line
            self.strbases = dna_sequence

    def max_base(self):
        bases_dict = {}
        for b in Seq.bases:
            bases_dict[b] = self.count_base(b)
        most_frequent_base = max(bases_dict, key=bases_dict.get)

        return most_frequent_base
class Gene(Seq):
    def __init__(self, strbases, name=""):
        super().__init__(strbases)
        self.name = name
        print("New gene created")

    def __str__(self):
        return self.name + "-" + self.strbases
