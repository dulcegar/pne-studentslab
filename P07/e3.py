import http.client
import json
from http import HTTPStatus

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

#nos piden hacer una consulta del gen mir633 y el servidor de ensembl nos tiene que devolver la informacion de dicho gen
GENE = "MIR633"
SERVER = 'rest.ensembl.org'
RESOURCE = f'/sequence/id/{GENES[GENE]}'  #hay que meterle el identificador correspondiente (el id) es decir, numeritos
PARAMS = '?content-type=application/json'
URL = SERVER + RESOURCE + PARAMS

print()
print(f"SERVER: {SERVER}")
print(f"URL: {URL}")

conn = http.client.HTTPConnection(SERVER)

try:   #hacemos la peticion
    conn.request("GET", RESOURCE + PARAMS)
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

response = conn.getresponse()  #tenemos la respuesta
print(f"Response received!: {response.status} {response.reason}\n")
if response.status == HTTPStatus.OK:
    data_str = response.read().decode("utf-8")   #leo lo q m llega como string y lo traduzco
    print(data_str) #para ver la info q nos llega y saber q pedir dependiendo de lo q nos pidan en el ejercicio
    data = json.loads(data_str) #lo convierto en diccionario y json, previamente haciedno un print de la info q nos llega
    print() #espacio en blanco pa separar
    print(f"Gene: {GENE}")
    print(f"Description: {data['desc']}")
    print(f"Bases: {data['seq']}")