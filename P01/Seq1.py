class Seq:
    bases = ["A", "C", "T", "G"]

    def __init__(self, strbases = None):
        if strbases is None or len(strbases) == 0:
            self.strbases = "NULL"
            print ("NULL sequence created")

        else:
            ok = True
            for b in strbases:
                if b not in Seq.bases:
                    ok = False
                    self.strbases = "ERROR!"
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

class Gene(Seq):
    def __init__(self, strbases, name=""):
        super().__init__(strbases)
        self.name = name
        print("New gene created")

    def __str__(self):
        return self.name + "-" + self.strbases
