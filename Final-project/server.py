import http.server
from http import HTTPStatus
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import jinja2
import os
import json
import http.client


PORT = 8080
HTML_FOLDER = "html"
EMSEMBL_SERVER = "rest.ensembl.org" #nos almacenamos la ip del servidor de ensembl
RESOURCE_TO_ENSEMBL_REQUEST = {
    '/listSpecies': {'resource': "/info/species", 'params': "content-type=application/json"}
}   #diccionario que tiene como clave un recurso, pasa de recurso a ensembl y dentro de el hay otro diccionario, le pasamos el recurso/endpoint/path y asi sepa que recurso de ensembl hay q utilizar y q parametros me tiene q pasar
RESOURCE_NOT_AVAILABLE_ERROR = "Resource not available"
ENSEMBL_COMMUNICATION_ERROR = "Error in communication with the Ensembl server"


def read_html_template(file_name):
    file_path = os.path.join(HTML_FOLDER, file_name)
    contents = Path(file_path).read_text()
    contents = jinja2.Template(contents)
    return contents


def server_request(server, url): #esta funcion nos permite pedirle algo al servidor de ensembl y q nos conteste

    error = False
    data = None
    try:
        connection = http.client.HTTPSConnection(server)
        connection.request("GET", url)
        response = connection.getresponse()
        if response.status == HTTPStatus.OK:
            json_str = response.read().decode()
            data = json.loads(json_str)
    except Exception:  # Comment
        error = True
    return error, data


def handle_error(endpoint, message): #le mandamos el resource(endpoint) y el mensaje que varia segun el error
    context = {
        'endpoint': endpoint,
        'message': message
    }
    return read_html_template("error.html").render(context=context)


def list_species(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
    url = f"{request['resource']}?{request['params']}"
    error, data = server_request(EMSEMBL_SERVER, url)
    if not error:
        limit = None
        if 'limit' in parameters:
            limit = int(parameters['limit'][0])
        species = data['species']  # list<dict>
        name_species = []
        for specie in species[:limit]:
            name_species.append(specie['display_name'])
        context = {
            'number_of_species': len(species),
            'limit': limit,
            'name_species': name_species
        }
        contents = read_html_template("species.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE  # Comment
    return code, contents


socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path  #resource or path
        print(f"Endpoint: {endpoint}")
        parameters = parse_qs(parsed_url.query)
        print(f"Parameters: {parameters}")

        code = HTTPStatus.OK #de primeras esta variable y si hay error lo cambiamos ahi
        content_type = "text/html"
        contents = ""
        if endpoint == "/":  #en vez de resource o path, endpoint
            file_path = os.path.join(HTML_FOLDER, "index.html")
            contents = Path(file_path).read_text()
        elif endpoint == "/listSpecies":
            code, contents = list_species(endpoint, parameters)
        elif endpoint == "/karyotype":
            pass
        elif endpoint == "/chromosomeLength":
            pass
        else:
            contents = handle_error(endpoint, RESOURCE_NOT_AVAILABLE_ERROR) #handle_error = manejar el error y le pasamos la variable de resource_not...
            code = HTTPStatus.NOT_FOUND

        self.send_response(code) #lo ponemos aqui una sola vez en vez de en cada if/elif
        contents_bytes = contents.encode()
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)

#PROGRAMA PRINCIPAL
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()  #es un metodo que contiene TCPServer
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()