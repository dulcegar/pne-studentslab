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
EMSEMBL_SERVER = "rest.ensembl.org"
RESOURCE_TO_ENSEMBL_REQUEST = {
    '/listSpecies': {'resource': "/info/species", 'params': "content-type=application/json"},
    '/karyotype': {'resource': "/info/assembly", 'params': "content-type=application/json"},
    '/chromosomeLength': {'resource': "/info/assembly", 'params': "content-type=application/json"},
    '/geneSeq': {'resource': "/sequence/id", 'params': "content-type=application/json"},
    '/geneInfo': {'resource': "/overlap/id", 'params': "content-type=application/json;feature=gene"},
    '/geneCalc': {'resource': "/sequence/id", 'params': "content-type=application/json"},
    '/sequence': {'resource': "/sequence/id", 'params': "content-type=application/json;db_type=otherfeatures;type=cds;object_type=transcript"}
}
RESOURCE_NOT_AVAILABLE_ERROR = "Resource not available"
ENSEMBL_COMMUNICATION_ERROR = "Error in communication with the Ensembl server"
GENE_ERROR = "Gene not found"


def read_html_template(file_name):
    file_path = os.path.join(HTML_FOLDER, file_name)
    contents = Path(file_path).read_text()
    contents = jinja2.Template(contents)
    return contents


def server_request(server, url):

    error = False
    data = None
    try:
        conn = http.client.HTTPSConnection(server)
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status == HTTPStatus.OK:
            json_str = response.read().decode()
            data = json.loads(json_str)
        else:
            error = True
    except Exception:
        error = True
    return error, data


def handle_error(endpoint, message):
    d = {
        'endpoint': endpoint,
        'message': message
    }
    return read_html_template("error.html").render(context=d)


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
        code = HTTPStatus.SERVICE_UNAVAILABLE
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
        chromosomes = data["top_level_region"]
        chromo_length = None
        for chromosome in chromosomes:
            if chromosome['name'] == chromo:
                chromo_length = chromosome['length']
                break
        context = {
            'chromo': chromo,
            'length': chromo_length
        }

        contents = read_html_template("chromosome_length.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents


def get_id(gene):
    resource = "/homology/symbol/human/" + gene
    params = 'content-type=application/json;format=condensed'
    url = f"{resource}?{params}"
    error, data = server_request(EMSEMBL_SERVER, url)
    gene_id = None
    if not error:
        gene_id = data['data'][0]['id']

    return gene_id


def geneSeq(parameters):
    endpoint = '/geneSeq'
    gene = parameters['gene'][0]
    gene_id = get_id(gene)
    print(f"Gene: {gene} - Gene ID: {gene_id}")
    if gene_id is not None:
        request = RESOURCE_TO_ENSEMBL_REQUEST[endpoint]
        url = f"{request['resource']}/{gene_id}?{request['params']}"
        error, data = server_request(EMSEMBL_SERVER, url)
        if not error:
            bases = data['seq']
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

def sequence(parameters):
    code = None
    content_type = None
    contents = None
    id = parameters['id'][0]
    species = parameters['species'][0]
    even_bases = "even_bases" in parameters
    endpoint = f"/sequence/id/{id}"
    params = "content-type=application/json;db_type=otherfeatures;type=cds;object_type=transcript"
    url = f"{endpoint}?{params};species={species}"
    error, data = server_request(EMSEMBL_SERVER, url)
    if not error:
        bases = data['seq']
        length = len(bases)
        if length % 2 == 0:
            is_even = True
        else:
            is_even = False
        context = {
            'id': id,
            'species': species,
            'length': length,
            'is_even': is_even,
            'even_bases': even_bases,
            'bases': str(bases)
        }
        contents = read_html_template("sequence.html").render(context=context)
        code = HTTPStatus.OK
    else:
        contents = handle_error(endpoint, ENSEMBL_COMMUNICATION_ERROR)
        code = HTTPStatus.SERVICE_UNAVAILABLE
    return code, contents, content_type



socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)
        endpoint = parsed_url.path
        print(f"Endpoint: {endpoint}")
        parameters = parse_qs(parsed_url.query)
        print(f"Parameters: {parameters}")

        code = HTTPStatus.OK
        content_type = "text/html"
        contents = ""
        if endpoint == "/":
            file_path = os.path.join(HTML_FOLDER, "index.html")
            contents = Path(file_path).read_text()
        elif endpoint == "/listSpecies":
            code, contents = list_species(endpoint, parameters)
        elif endpoint == "/karyotype":
            code, contents = karyotype(endpoint, parameters)
        elif endpoint == "/chromosomeLength":
            code, contents = chromosome_length(endpoint, parameters)
        elif endpoint == "/geneSeq":
            code, contents = geneSeq(parameters)
        elif endpoint == "/geneInfo":
            code, contents = geneInfo(parameters)
        elif endpoint == "/geneCalc":
            code, contents = geneCalc(endpoint, parameters)
        elif endpoint == "/geneList":
            code, contents = geneList(parameters)
        elif endpoint == "/sequence":
            code, contents, content_type = sequence(parameters)
        else:
            contents = handle_error(endpoint, RESOURCE_NOT_AVAILABLE_ERROR)
            code = HTTPStatus.NOT_FOUND

        self.send_response(code)
        contents_bytes = contents.encode()
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)


#PROGRAMA PRINCIPAL
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()