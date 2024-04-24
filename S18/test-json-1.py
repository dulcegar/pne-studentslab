import json  #nuevo. herramientas para trabajar cn json
import termcolor
from pathlib import Path

json_string = Path("people-1.json").read_text()  #abrimos el fichero de json y lo leemos y lo almacenamos en la variable json_string (est aen formato string)
person = json.loads(json_string)   #nos creamos una variable con la funcion json.loads (nueva) con la q coge nuestra string y traduce en un diccionario en phyton, por lo que person es un diccionario
#BASICAMENTE CONVERTIMOS EL JSON EN DICCIONARIO PARA USARLO COMO TAL

firstname = person['Firstname']  #esta linea almacena en la variable firstname el nombre de el diccionario que acabamos d crear con el json que hemos cogido
lastname = person['Lastname']  #ahora de nuestro diccionario cogemos lastname
age = person['Age']

print()
termcolor.cprint("Name: ", 'green', end="")
print(firstname, lastname)
termcolor.cprint("Age: ", 'green', end="")
print(age)