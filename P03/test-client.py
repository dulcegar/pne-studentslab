#este nos lo creo javier y sirve para poder probarlo en nuestro servidor

from client import Client

PRACTICE = 3
EXERCISE = 7
SERVER_IP = "192.168.0.33"
SERVER_PORT = 8080
N = 5
BASES = "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA"
GENES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")


c = Client(SERVER_IP, SERVER_PORT)  #creamos el cliente
print(c)

print("* Testing PING...")
response = c.talk("PING")
print(response)

print("* Testing GET...")
for n in range(N): #desde 0 a 4
    response = c.talk(f"GET {n}") #le enviamos el comando al servidor (lo q le sale al servidor)
    print(f"GET {n}: {response}") #lo que se pinta en el cliente

print() #esto es para qye haya un conjunto vacio en el formato q se pinta

print("* Testing INFO...")
response = c.talk(f"INFO {BASES}")
print(response)

print()

print("* Testing COMP...")
print(f"COMP {BASES}")
response = c.talk(f"COMP {BASES}")
print(response)

print()

print("* Testing REV...")
print(f"REV {BASES}")
response = c.talk(f"REV {BASES}")
print(response)

print()

print("* Testing GENE...")
for gene in GENES:
    print(f"GENE {gene}")
    response = c.talk(f"GENE {gene}")
    print(response)
    print()
