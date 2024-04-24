# -- Example of a client that uses the HTTP.client library
# -- for requesting the main page from the server
import http.client   #me piden que yo me cree mi propio cliente http, osea que no use safari o firefox sino que lo veamos aqui, el navegador web es el cliente, ahora nos vamos a crear el nuestro propio aqui

PORT = 8080
SERVER = 'localhost'  #localhost = 127.0.0.1

print(f"\nConnecting to server: {SERVER}:{PORT}\n")

# Connect with the server (NUEVO)
conn = http.client.HTTPConnection(SERVER, PORT) #creamos una conexion cn el servidor, nos creamos un objeto de la clase HTTOConection (q esta dentro de el http.client, por eso es nuevo)

# -- Send the request message, using the GET method. We are
# -- requesting the main page (/)
try:
    conn.request("GET", "/")  #cogemos la conexion que acabamos de crear y ejecutamos la funcion rquest, le estamos haciendo al servidor una peticion del tipo Get y le pedimos la / , es decir la pagina principal
except ConnectionRefusedError:
    print("ERROR! Cannot connect to the Server")
    exit()   #el exit sale cortando el codigo por aqui, osea no se ejecutaria lo d abajo

# -- Read the response message from the server
#si el servidor me responde, cojo la rspuesta cn el getresponse
r1 = conn.getresponse()  #para obtener la respuesta del servidor usamos getresponse, r1 es un pbjeto de la clase HTTPResponse, es decir dentro tiene propiedades y yo puedo acceder a sus atributos...

# -- Print the status line
print(f"Response received!: {r1.status} {r1.reason}\n")  #el r1.reason es el texto asociado al cogido (200=OK...)

# -- Read the response's body
data1 = r1.read().decode("utf-8")

# -- Print the received data
print(f"CONTENT: {data1}")