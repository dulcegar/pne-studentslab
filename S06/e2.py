from seq import Seq

seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]

'''
for s in seq_list:
    print(f"Sequence {seq_list.index(s)}: (Length: {s.len()}) {s}")
'''
#otra forma
for i, s in enumerate(seq_list):   #enumerate crea una lista nueva y la enumera empezando por 0
    print(f"Sequence {i}: (Length: {s.len()}) {s}")