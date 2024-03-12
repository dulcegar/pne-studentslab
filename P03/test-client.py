#este nos lo creo javier y sirve para poder probarlo en nuestro servidor

from client import Client

SERVER_IP = "192.168.0.33"
SERVER_PORT = 8080

c = Client(SERVER_IP, SERVER_PORT)  #creamos el cliente
response = c.talk("PING")  #el .talk es para abrir un socket hacer nsq y cerrarlo
print(response)
response = c.talk("GET 2")
print(response)
response = c.talk("INFO AACCGTA")
print(response)
response = c.talk("COMP AACCGTA")
print(response)
response = c.talk("REV AACCGTA")
print(response)
response = c.talk("GENE U5")
print(response)