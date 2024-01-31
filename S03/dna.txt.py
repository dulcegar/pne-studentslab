def read_txt_file(filename):
    with open(filename, "r") as f:
        total_num_bases = 0
        letters = {"A": 0, "C": 0, "G": 0, "T": 0}
        for line in f:
            total_num_bases += len(line)
            for i in line:
                if i in letters:
                    letters[i] += 1

    print(f"Total number of bases: {total_num_bases}")
    for k, v in letters.items():
        print(k + ":", v)

read_txt_file("dna")
