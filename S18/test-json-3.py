#en este en el people-3.json hay diccionarios dentro de el, es decir, diccionarios dentro de un diccionario
import json
import termcolor
from pathlib import Path

json_string = Path("people-3.json").read_text()
person = json.loads(json_string)

firstname = person['Firstname']
lastname = person['Lastname']
age = person['Age']
phoneNumbers = person['PhoneNumbers'] #en este ejercicio esto se convierte en una lista de diccionarios

print()
termcolor.cprint("Name: ", 'green', end="")
print(firstname, lastname)
termcolor.cprint("Age: ", 'green', end="")
print(age)

termcolor.cprint("Phone numbers: ", 'green', end='')
print(len(phoneNumbers))

for i, phone in enumerate(phoneNumbers):   #estamos enumerando la lista de diccionarios, por lo que ahora tenemos una lista cuyos elementos son diccionarios y su posicion en la lista
    termcolor.cprint("  Phone {}:".format(i), 'blue')

    termcolor.cprint("    Type: ", 'red', end='')
    print(phone['type'])   #consultamos el valor asociado a la clave type, lo ponemos asi porq es un diccionario
    termcolor.cprint("    Number: ", 'red', end='')
    print(phone['number'])