import http.server
from http import HTTPStatus  #delmodulo http importa el httpstatus q contiene constantes con los modulos de http (200, 404..) en vez de usarlos o ponerlos usamos esto, osea ponemos http.status.OK
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import jinja2
import os
from seq import Seq  #del modulo seq.py incluye Seq para q el servidor pueda crearse secuencias de ADN


PORT = 8080
HTML_FOLDER = "html"
SEQUENCES = ["CATGA", "TTACG", "AAAAA", "CGCGC", "TATAT"]
GENES = ["ADA", "FRAT1", "FXN", "RNU6_269P", "U5"]
OPERATIONS = ["info", "comp", "rev"]


def read_html_template(file_name):
    file_path = os.path.join(HTML_FOLDER, file_name) #recib el nombre de un fichero dentro de la carpeta html
    contents = Path(file_path).read_text() #lee el fichero
    contents = jinja2.Template(contents)  #nos creamos un objeto de la clase Template del jinja dos a la que le pasamos la variable contents
    return contents  #devolvemos el valor de la clase contents, es decir el objeto de la clase Template de la plantilla que yo le mandado


def handle_get(arguments):  #basicamente es para poner el codigo de do_GET mas bonito
    try:
        sequence_number = int(arguments['sequence_number'][0]) #accedemos al valor asociado a arguments, lo cambiamos a int porq queremos pedir una posicion de la lista
        contents = read_html_template("get.html")  #llamo a la funcion de antes (read_html_template) porq necesitamos tdo lo q tiene dentro
        context = {'number': sequence_number, 'sequence': SEQUENCES[sequence_number]} #de la lista SEQUENCES se mete en la posicion que pidan
        contents = contents.render(context=context)
        code = HTTPStatus.OK  #como hemos importado el http, podemos usar esto en vez del 200
    except (KeyError, IndexError, ValueError):
        file_path = os.path.join(HTML_FOLDER, "error.html")
        contents = Path(file_path).read_text()
        code = HTTPStatus.NOT_FOUND
    return contents, code


socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)  #trocea la ruta que recibimos cuando el cliente manda una peticion
        resource = parsed_url.path  #tbn podemos llamar a la variable path
        print(f"Resource: {resource}")  #si el cliente le da al boton ping, se recibe /ping
        arguments = parse_qs(parsed_url.query) #un diccionario con los argumentos/parametros que nos llega en la peticion
        print(f"Arguments: {arguments}")

        if resource == "/":  #or resource == "/index.html":
            contents = read_html_template("index.html")
            context = {'n_sequences': len(SEQUENCES), 'genes': GENES} #esto es lo q luego usamos en el html (el n_sequences y el genes)
            contents = contents.render(context=context) #le decimos que se renderice=actualice
            self.send_response(200)
        elif resource == "/ping": #en este no llamamos al read_html_template xqe no hay variables que leer
            file_path = os.path.join(HTML_FOLDER, "ping.html")
            contents = Path(file_path).read_text()   #creo el objeto de tipo path con esa ruta (file_path)
            self.send_response(200)  #tbn se podrias poner self.send_response(HTTPStatus.OK)
        elif resource == "/get":
            contents, code = handle_get(arguments)   #hay dos variables a la izq del = porq lo q nos devuelve el handle_get es una dupla, nos devuelve dos cosas, la 1 una cadena de caractereces y la 2 es un numero entero
            self.send_response(code)
        elif resource == "/gene":
            try:
                gene_name = arguments['gene_name'][0] #no lo convierto a un entero xqe estamos pidiendo un string (frat1, ada...)
                file_path = os.path.join(HTML_FOLDER, "gene.html")
                contents = Path(file_path).read_text()
                contents = jinja2.Template(contents)
                file_name = os.path.join("..", "sequences", gene_name) #para meterse en la carpeta sequences ( q esya fuera de la practica 6)
                s = Seq() #crea un objeto de la clase Seq de secuencia nula, no tiene valor aun strbases
                s.read_fasta(file_name)  #se le da valor a strbases
                context = {'gene_name': gene_name, 'sequence': str(s)} #se pone el nombre del gene q hemos pedido y luego se convierte en string la secuencia
                contents = contents.render(context=context)
                self.send_response(200)
            except (KeyError, IndexError, FileNotFoundError):
                file_path = os.path.join(HTML_FOLDER, "error.html")
                contents = Path(file_path).read_text()
                self.send_response(404)
        elif resource == "/operation":  #en este tipo el cliente manda dos cosas, las bases y op
            try:
                bases = arguments['bases'][0] #basicamente coge lo que introduce el cliente en el campo de texto
                op = arguments['op'][0]  # lower()   #le mandamos la operacion q haya puesto el cliente, el op puede ser info, comp o rev (MINUSCULAS)
                contents = read_html_template("operation.html")
                s = Seq(bases) #nos creamos un objeto de la clase Seq con las bases que haya mandado el cliente
                if op in OPERATIONS:  #si la operacion que quiere el usuario esta en la lista de arriba (dnd hemos puesto las tres q usamos), este if es por si el usuario intenta trolearnos a traves de la url
                    if op == "info":
                        result = s.info().replace("\n", "<br><br>")  #nos devuelve lo que tiene el def info en seq, con el replace sustituimos cada /n con dos saltos de linea pero en html
                    elif op == "comp":
                        result = s.complement()  #cogemos el objeto de seq y llamamos a complement
                    else:  # elif op == "rev":
                        result = s.reverse()
                    context = {'sequence': str(s), 'op': op, 'result': result} #creamos el contexto para comunicarnos con ña pagina web y q luego se sustituya
                    contents = contents.render(context=context)
                    self.send_response(200)
                else:
                    file_path = os.path.join(HTML_FOLDER, "error.html")
                    contents = Path(file_path).read_text()
                    self.send_response(404)
            except (KeyError, IndexError):
                file_path = os.path.join(HTML_FOLDER, "error.html")
                contents = Path(file_path).read_text()
                self.send_response(404)
        else:
            file_path = os.path.join(HTML_FOLDER, "error.html")
            contents = Path(file_path).read_text()
            self.send_response(404)

        contents_bytes = contents.encode() #transformacion de nuestro body a bytes
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)


with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()

