import http.client
import json
from http import HTTPStatus
from seq import Seq  #aqui ahora usamos el seq

#en este, el usuario introduce el nombre de un gen y hace lo mismo q en el e3
GENES = {
    "FRAT1": "ENSG00000165879",
    "ADA": "ENSG00000196839",
    "FXN": "ENSG00000165060",
    "RNU6_269P": "ENSG00000212379",
    "MIR633": "ENSG00000207552",
    "TTTY4C": "ENSG00000228296",
    "RBMY2YP": "ENSG00000227633",
    "FGFR3": "ENSG00000068078",
    "KDR": "ENSG00000128052",
    "ANK2": "ENSG00000145362"
}

print()
gene = input("Write the gene name: ") #le pedimos al usuario el nombre de un gen
if gene in GENES: #comprobamos q el gen esta dentro del diccionario
    SERVER = 'rest.ensembl.org'
    RESOURCE = f'/sequence/id/{GENES[gene]}'
    PARAMS = '?content-type=application/json'
    URL = SERVER + RESOURCE + PARAMS

    print()
    print(f"SERVER: {SERVER}")
    print(f"URL: {URL}")

    conn = http.client.HTTPConnection(SERVER)

    try:
        conn.request("GET", RESOURCE + PARAMS)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    response = conn.getresponse()
    print(f"Response received!: {response.status} {response.reason}\n") #printamos el status y el reason
    if response.status == HTTPStatus.OK:
        data_str = response.read().decode("utf-8")
        data = json.loads(data_str)
        print(f"Gene: {gene}")
        print(f"Description: {data['desc']}")
        bases = data['seq'] #cogemos las bases de la secuencia
        s = Seq(bases) #nos creamos una variable nuestra de la clase seq
        print(s.info()) #llamamos al metodo info (dentro de seq) porq nos piden su informacion