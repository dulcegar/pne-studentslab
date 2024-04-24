import json
import termcolor
from pathlib import Path

json_string = Path("people-2.json").read_text()  #cogemos otro file
person = json.loads(json_string)  #convertimos en diccionario con json.loads

firstname = person['Firstname']
lastname = person['Lastname']
age = person['Age']
phoneNumbers = person['PhoneNumbers']  #esta variable va a ser una lista de numeros porque hay dos elementos

print()
termcolor.cprint("Name: ", 'green', end="")
print(firstname, lastname)
termcolor.cprint("Age: ", 'green', end="")
print(age)

termcolor.cprint("Phone numbers: ", 'green', end='')
print(len(phoneNumbers)) #nos dice la long d la lista, es decir 2

for i, num in enumerate(phoneNumbers):  #el enumerate traduce la lista en otra nueva dnd pone la posicion y  el valor de los numeros --> [(0, "1111"). (1, "2222")]
    termcolor.cprint(f"\tPhone {i}: ", 'blue', end='')  #\t es un tabulador
    print(num)