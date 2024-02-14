import os #operative system, nos permite interactuar con el sistema operativo
from seq0 import *

N = 20  #constante (variable) para hacer cambios, si nos piden 50 en vez de 20 solo cambiamos esta variable y ya

dna_file = input("DNA file: ") #en este ejercicio nos piden el u5 pero con este input podemos meter cualquiera
try:
    dna_sequence = seq_read_fasta(os.path.join("..", "sequences", dna_file)) #el os.path nos permite trabajar con rutas en el sistema operativo
    # .. sirve para retroceder, salimos de la carpeta p00 y luego entramos en sequences (despues de la ,)
    # el os.path.join sirve para que me funcione en linux, macos, windows o el q sea sin que de error
    #las , se traducen com barras, depende de si trabajo en lynux o macos o windows ws / o \
    # se mete en sequences y lgo en el dna_file que basicamente es el input de arriba