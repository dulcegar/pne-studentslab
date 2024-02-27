class Seq:
    bases = ["A", "C", "T", "G"]

    def __init__(self, strbases = None):
        if strbases is None:
            self.strbases = "NULL"
            print ("NULL sequence created")

        else:
            ok = True
            for b in strbases:
                if b not in Seq.bases:
                    ok = False
                    self.strbases = "ERROR!"
                    print("Incorrect sequence detected")
                    break
            if ok:
                self.strbases = strbases
                print("New sequence created!")

    def __str__(self):
        return self.strbases

    def len(self):
        return len(self.strbases)


class Gene(Seq):
    def __init__(self, strbases, name=""):
        super().__init__(strbases)
        self.name = name
        print("New gene created")

    def __str__(self):
        return self.name + "-" + self.strbases
