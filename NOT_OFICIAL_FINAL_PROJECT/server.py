import http.server
from http import HTTPStatus
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs, quote
import jinja2
import os
import json
import http.client


PORT = 8080
HTML_FOLDER = "html"
EMSEMBL_SERVER = "rest.ensembl.org" #nos almacenamos la ip del servidor de ensembl
RESOURCE_TO_ENSEMBL_REQUEST = {
    '/listSpecies': {'resource': "/info/species", 'params': "content-type=application/json"},
    '/karyotype': {'resource': "/info/assembly", 'params': "content-type=application/json"},
    '/chromosomeLength': {'resource': "/info/assembly", 'params': "content-type=application/json"}, #tiene el mismo resorce que el karyotupe porq cuando ponga print(data) me va  asalir la misma info
    '/geneSeq': {'resource': "/sequence/id", 'params': "content-type=application/json"}, #acabamos pidiendo el recurso id
    '/geneInfo': {'resource': "/overlap/id", 'params': "content-type=application/json;feature=gene"},
    '/geneCalc': {'resource': "/sequence/id", 'params': "content-type=application/json"}
}   #diccionario que tiene como clave un recurso, pasa de recurso a ensembl y dentro de el hay otro diccionario, le pasamos el recurso/endpoint/path y asi sepa que recurso de ensembl hay q utilizar y q parametros me tiene q pasar
RESOURCE_NOT_AVAILABLE_ERROR = "Resource not available"
ENSEMBL_COMMUNICATION_ERROR = "Error in communication with the Ensembl server"
GENE_ERROR = "Gene not found"


def read_html_template(file_name):
    file_path = os.path.join(HTML_FOLDER, file_name)
    contents = Path(file_path).read_text()
    contents = jinja2.Template(contents)
    return contents


def server_request(server, url): #esta funcion nos permite pedirle algo al servidor de ensembl y q nos conteste

    error = False #ponemos inicialmente q no va a haber error
    data = None
    try:
        conn = http.client.HTTPSConnection(server) #nos crea un objeto del tipo http.client.HTTPSConnection y le mandamos el server (nuestro)
        conn.request("GET", url) #coge el objeto y le hacemos una request del tipo GET y le pasamos la URL
        response = conn.getresponse()
        if response.status == HTTPStatus.OK:
            json_str = response.read().decode()
            data = json.loads(json_str)
        else:
            error = True
    except Exception:
        error = True
    return error, data


def handle_error(endpoint, message): #le mandamos el resource(endpoint) y el mensaje que varia segun el error
    d = {  #me creo un diccionario
        'endpoint': endpoint,
        'message': message
    }
    return read_html_template("error.html").render(context=d) #nos devuelve un string con el contenido de la plantilla html sustituyendo lo que es variable


def list_species(endpoint, parameters): #le pasamos esto al if de listspecies, las 4 siguientes lineas estaran en todas las deficiones (karyotype y chromosomalLength)
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint] #consulta que le hacemos al diccionario, le pasamos el endpoint (depende del if en el que nos metamos)
    url = f"{request['resource']}?{request['params']}" #nos almacenamos en la variable url un string con el request (diccionario), por un lado el resource y por otro los parametros
    error, data = server_request(EMSEMBL_SERVER, url) #nos hemos creado la funcion server_request q permite la comunicacion con el servidor de ensembl y asi no ponerlo tdo el rato en cada tipo de endpoint, y le pasamos a q servidor me voy a conectar y la url d la funcion, Nos devuelve si ha habido error en la comunicacion y los datos
    if not error:
        limit = None
        if 'limit' in parameters: #si mi diccionario con los parametros contiene la clave limit, me llega limite
            limit = int(parameters['limit'][0]) #le cambiamos el valor de limit (q en principio es None) y lo transformamos a un entero
        species = data['species']  # list<dict>
        name_species = [] #lista vacia
        for specie in species[:limit]: #con este for recorro la lista de diccionario (de especies) de especie en especie, lo de [:limit] es xqe lo estoy acotando
            name_species.append(specie['display_name']) #en esa lista me guardo el nombre asociado al display_name
        context = { #nos creamos un diccionario con el contexto con parejas clave-valor, que luego lo usamos en el html list_species
            'number_of_species': len(species),
            'limit': limit,
            'name_species': name_species
        }
        contents = read_html_template("species.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE  #decimos que el servicio que solicita no esta available
    return code, contents

def karyotype(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
    species = quote(parameters["species"][0])
    url = f"{request['resource']}/{species}?{request['params']}"
    error, data = server_request(EMSEMBL_SERVER, url)
    if not error:
        karyotype = data["karyotype"]
        species = species.replace("%20", " ")
        context = {
            'species': species,
            'karyotype': karyotype
        }
        contents = read_html_template("karyotype.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents


def chromosome_length(endpoint, parameters):
    request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
    species = parameters["species"][0]
    chromo = parameters["chromo"][0]
    url = f"{request['resource']}/{species}?{request['params']}"
    error, data = server_request(EMSEMBL_SERVER, url)
    if not error:
        print(data)
        chromosomes = data["top_level_region"]  #extraemos de data el valor asociado a la clave top_level_region. que nos da mas info de la que necesitamos. chromosomes es un diccionario cn muchas cosas
        chromo_length = None #inicialmente la longitud es ninguna, y en caso de q metamos un chromosome que no existe, nos pondria none
        for chromosome in chromosomes:
            if chromosome['name'] == chromo:   #si el chromosome (diccionario) tiene como valor el nombre name q es igual al chromo (q es lo q m han mandado). el nombre de unos de los cromosomas coincide con el chromo que me han mandado entro en el if
                chromo_length = chromosome['length'] #me almaceno en la variable length la longitud de ese chromosoma
                break  #para salir de forma abrupta
        context = {
            'chromo': chromo,
            'length': chromo_length
        }
        #a partir de aqui es en tds igual salvo en...
        contents = read_html_template("chromosome_length.html").render(context=context) #esta linea que cm¡ambiamos el nombre del html
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents


def get_id(gene): #funcion que dado el nombre de un gen consulta al servidor de ensembl cual es su identificador asociado (ej: FRAT1: "EN0672382"), traduce del gen al identificador
    resource = "/homology/symbol/human/" + gene #el recurso que solicitamos al servidor de ensembl, porq son tds asociados al ser humano(specie) y le concatenamos el gene
    params = 'content-type=application/json;format=condensed' #en este el params es ditinto, le hemos indicado al final otro parametro mas
    url = f"{resource}?{params}"
    error, data = server_request(EMSEMBL_SERVER, url)
    gene_id = None #gene_id no es nada
    if not error: #si no hay error, tambien sirve para controlar errores, si nos mandan un gen no humano
        gene_id = data['data'][0]['id'] # 'data' (lista) esta dentro del diccionario data y dentro de la lista 'data', sobre esa lista entramos a la posicion 0, q es un diccionario y sobre ese diccionario entramos a id
        #tengo data, y dentro de esa lista hay un diccionario en la primera posicion
    return gene_id


def geneSeq(parameters):
    endpoint = '/geneSeq'
    gene = parameters['gene'][0]
    gene_id = get_id(gene)  #el get_id es una funcion que dado el nombre de un gen consulta al servidor de ensembl cual es su identificador asociado
    print(f"Gene: {gene} - Gene ID: {gene_id}") #pinto el nombre del gen y su identificador, simplemente para verlo en el servidor
    if gene_id is not None: #si la variable gene_id tiene contenido, es decir, si es distinto de None
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}/{gene_id}?{request['params']}" #construyo la url con el id, para ahora poder hacer la culta buena con el identificador del gen que nos manden, por eso hacemos antes lo de get_id
        error, data = server_request(EMSEMBL_SERVER, url) #peticion al servidor de ensembl
        if not error:
            bases = data['seq'] #dentro de la data q me da ensembl tiene que haber un diccionario llamado seq, con todas las bases de la secuencia para que me las mande
            context = {
                'gene': gene,
                'bases': bases
            }
            contents = read_html_template("gene_seq.html").render(context=context)
            code = HTTPStatus.OK
        else:
            contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
            code = HTTPStatus.SERVICE_UNAVAILABLE
    else:
        contents = handle_error(endpoint, GENE_ERROR)
        code = HTTPStatus.NOT_FOUND
    return code, contents


def geneInfo(parameters):
    endpoint = '/geneInfo'
    gene = parameters['gene'][0]
    gene_id = get_id(gene)
    print(f"Gene: {gene} - Gene ID: {gene_id}")
    if gene_id is not None:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}/{gene_id}?{request['params']}"
        error, data = server_request(EMSEMBL_SERVER, url)
        if not error:
            print(f"geneInfo: {data}")
            data = data[0]
            start = data['start']
            end = data['end']
            length = end - start
            id = gene_id
            chromosome_name = data['assembly_name']
            context = {
                'gene': gene,
                'start': start,
                'end': end,
                'length': length,
                'id': id,
                'chromosome_name': chromosome_name
            }
            contents = read_html_template("gene_info.html").render(context=context)
            code = HTTPStatus.OK
        else:
            contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
            code = HTTPStatus.SERVICE_UNAVAILABLE
    else:
        contents = handle_error(endpoint, GENE_ERROR)
        code = HTTPStatus.NOT_FOUND
    return code, contents

def geneCalc(endpoint, parameters):
    gene = parameters["gene"][0]
    gene_id = get_id(gene)
    print(f"Gene: {gene} - Gene ID: {gene_id}")
    if gene_id is not None:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}/{gene_id}?{request['params']}"
        error, data = server_request(EMSEMBL_SERVER, url)
        if not error:
            print(f"geneInfo: {data}")
            sequence = data["seq"]
            A = 0
            C = 0
            G = 0
            T = 0
            for base in sequence:
                if base == "A":
                    A += 1
                elif base == "C":
                    C += 1
                elif base == "G":
                    G += 1
                elif base == "T":
                    T += 1
            total = A + C + G + T
            base_A = round((A / total) * 100, 2)
            base_C = round((C / total) * 100, 2)
            base_G = round((G / total) * 100, 2)
            base_T = round((T / total) * 100, 2)

            context = {
                "gene": gene,
                "total_length": total,
                "A": base_A,
                "C": base_C,
                "G": base_G,
                "T": base_T,

            }
            contents = read_html_template("gene_calc.html").render(context=context)
            code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents


def geneList(parameters):
    chromo = parameters['chromo'][0]
    start = int(parameters['start'][0])
    end = int(parameters['end'][0])
    endpoint = f"/overlap/region/human/{chromo}:{start}-{end}"
    params = "content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon"
    url = f"{endpoint}?{params}"
    error, data = server_request(EMSEMBL_SERVER, url)
    print(data)
    if not error:
        data = data[0]
        chromo = int(data["seq_region_name"])
        start = data["start"]
        end = data["end"]
        genes_list = []
        for gene in data:
            if "external_name" in gene:
                name = data["external_name"]
                genes_list.append(name)
        context = {
            "chromo": chromo,
            "start": start,
            "end": end,
            "gene_list": genes_list[0]
        }
        contents = read_html_template("gene_list.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
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
            code, contents = list_species(endpoint, parameters) #le pasamos el endpoint y los parametros, podriamos no pasarle el endpoint y meterselo dentro de cada funcion como una variable
        elif endpoint == "/karyotype":
            code, contents = karyotype(endpoint, parameters)
        elif endpoint == "/chromosomeLength":
            code, contents = chromosome_length(endpoint, parameters)
        elif endpoint == "/geneSeq":
            code, contents = geneSeq(parameters) #en el nivel medio lo hacemos de otra forma, le paso solo los parametros y el endpoint lo meto en su def
        elif endpoint == "/geneInfo":
            code, contents = geneInfo(parameters)
        elif endpoint == "/geneCalc":
            code, contents = geneCalc(endpoint, parameters)
        elif endpoint == "/geneList":
            code, contents = geneList(parameters)
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