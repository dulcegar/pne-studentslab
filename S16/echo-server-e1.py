import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs #el modulo sirve para gestionar y tratar las peticiones que hace un cliente al servidor, parse es un submodulo dentro de urllib, parse sirve para tratar o analizar url, e importamos dos funciones
import jinja2 as j #nos permite generar una pag web dinamica, en lugar de referirnos a el como jinja2 lo llamos j.
import os


def read_html_file(file_name): #le pasamos el nombre del fichero
    file_path = os.path.join(HTML_FOLDER, file_name) #contruimos la ruta al fichero
    contents = Path(file_path).read_text() #creamos el objeto
    contents = j.Template(contents) #cogemos del modulo jinja2 una clase llamada Template a la q le pasamos contents (q es un string cn el cogigo html), nos estamos creando un objeto q es una plantilla q coge como base el codigo html
    return contents #devolvemos el objeto de tipo plantilla


PORT = 8080
HTML_FOLDER = "html"

socketserver.TCPServer.allow_reuse_address = True #reutilizar la direccion


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        url_path = urlparse(self.path) #le pasamos el self.path, en el urlparse tenemos mucha info del path
        print(f"URL PATH: {url_path}") #estos print no sirven para nada pero lo usamos para ver que hace
        resource = url_path.path #almacenamos en path el path de url_path
        print(f"Path: {resource}") #no sirve de nada, solo para ver que sirve
        arguments = parse_qs(url_path.query) #accedemos a la funcion query (la consulta) y me devuelve u resultado que lo guardamos en arguments
        print(f"Arguments: {arguments}") #para ver q hace, pero al final nos da un argumentos msg con una lista de valores.
        #con el urlparse y parse_qs tenemos por un lado el resource y por el otro los arguments para trabajar con ellos.

        if resource == "/": #el cliente no manda nada y le volvemos a mandar el formulario
            file_path = os.path.join(HTML_FOLDER, "form-e1.html")
            contents = Path(file_path).read_text()
            self.send_response(200)
        elif resource == "/echo": #esto significa que el cliente le ha mandado algo (ha escrito algo y dado a send)
            try:
                msg_param = arguments['msg'][0] #el arguments['msg'] nos devuelve una lista y sobre esa lista estoy cogiendo el valor que ocupa la posicion 0
                print(msg_param) #lo printeo para verlo
                contents = read_html_file("result-echo-server-e1.html").render(context={"todisplay": msg_param}) #dsd el codigo en python nos comunicamos cn el html
                #read_html_file lee el fichero html y le paso el nombre de un fichero (no lo pide pero lo uso)
                #read_html_file("result-echo-server-e1.html") esto es un objeto del tipo plantilla que tiene como base el html
                #le decimos a la plantilla que se renderice (el render es un metodo de la clase Template de jinja2), le pasamos el context (q es un diccionario q nos permite la comunicacion de python y la url) y a todisplay le estamos dando el valor que valga msg_param

                #si no usaramos el jinja2 tendriamos que crearnos este html:
                # contents = f"""  #es una variable q vale un string
                #     <!DOCTYPE html>
                #     <html lang="en">
                #         <head>
                #             <meta charset="utf-8">
                #             <title>Result</title>
                #         </head>
                #         <body>
                #             <h1>Received message:</h1>
                #             <p>{msg_param}</p>  #el msg_param es variable
                #             <a href="/">Main page</a>
                #         </body>
                #     </html>"""
                self.send_response(200)
            except (KeyError, IndexError):
                file_path = os.path.join(HTML_FOLDER, "error.html")
                contents = Path(file_path).read_text()
                self.send_response(404)
        else:
            file_path = os.path.join(HTML_FOLDER, "error.html")
            contents = Path(file_path).read_text()
            self.send_response(404)

        contents_bytes = contents.encode()
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)

#MAIN --> como siempre
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()