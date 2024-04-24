import http.client
import json
from http import HTTPStatus

#NOS COMUNICAMOS CON EL SERVIDOR DE ENSEMBL
#los ingredientes de la url
SERVER = 'rest.ensembl.org'  #el servidor no cambia
RESOURCE = '/info/ping'  #contante del recurso que solicitamos, este cambia siempre dependiendo del recurso que nos pidan
PARAMS = '?content-type=application/json'  #otra constante cn los parametros de la peticion, es decir lo que va a prtir de ?
URL = SERVER + RESOURCE + PARAMS  #compomgo la url porq cnd hagamos de cliente metemos esta url

print()
print(f"SERVER: {SERVER}")
print(f"URL: {URL}")

conn = http.client.HTTPConnection(SERVER)

try:
    conn.request("GET", RESOURCE + PARAMS)  #no ponemos la url xqe va cn el servidor por delante
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()

response = conn.getresponse() #me almaceno en response la info q m llega
print(f"Response received!: {response.status} {response.reason}\n")
if response.status == HTTPStatus.OK:   #para saber si la peticion ha ido bien (==200)
    data_str = response.read().decode("utf-8")  #no hace falta realmente poner el utf-8
    data = json.loads(data_str) #hacemos un loads, es decir q en data tenemos un diccionario
    print(data) #para saber la estructura del diccionario que manda el ensembl para saber que tiene dentro y que me interesa
    ping = data['ping'] #accedemos a una clave q se llama ping, pero pa saber esto nos tenemos q hacer antges un print de lo que tiene data para saber q nos interesa del servidor ensembl
    if ping == 1:   #ponemos == 1 porq es lo q nos dan ellos
        print("PING OK! The database is running!")
    else:
        print("...")