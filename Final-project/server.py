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

# Configuration    CAMBIAR ESTO Y EN VEZ DE LAS VARIABLES PONER A CASCOPORRO EL TEXTO EN CADA UNO
SERVER_PORT = 8080
HTML_FOLDER = "html"
ENSEMBL_API_SERVER = "rest.ensembl.org"
ERROR_RESOURCE_UNAVAILABLE = "Resource unavailable"
ERROR_COMMUNICATION_ENSEMBL = "Communication error with Ensembl server"
ERROR_GENE_NOT_FOUND = "Gene not found"


def load_template(template_name):
    template_path = os.path.join(HTML_FOLDER, template_name)
    template_content = Path(template_path).read_text()
    return jinja2.Template(template_content)


def fetch_data_from_server(api_server, api_endpoint):

    has_error = False
    response_data = None
    try:
        connection = http.client.HTTPSConnection(api_server)
        connection.request("GET", api_endpoint)
        api_response = connection.getresponse()
        if api_response.status == HTTPStatus.OK:
            json_response = api_response.read().decode()
            response_data = json.loads(json_response)
        else:
            has_error = True
    except Exception:
        has_error = True
    return has_error, response_data


def generate_error_page(api_endpoint, error_message):
    context = {
        'api_endpoint': api_endpoint,
        'error_message': error_message
    }
    return load_template("error.html").render(context=context)


def fetch_species_list(api_endpoint, params):
    api_resource = "/info/species"
    query_params = "content-type=application/json"
    api_url = f"{api_resource}?{query_params}"
    error_occurred, api_data = fetch_data_from_server(ENSEMBL_API_SERVER, api_url)

    if not error_occurred:
        species_limit = None

        if 'limit' in params:
            species_limit = int(params['limit'][0])
        species_list = api_data['species']  # list<dict>
        species_names = []

        for species in species_list[:species_limit]:
            species_names.append(species['display_name'])
        context = {
            'total_species': len(species_list),
            'species_limit': species_limit,
            'species_names': species_names
        }
        rendered_content = load_template("species.html").render(context=context)
        response_code = HTTPStatus.OK

    else:
        rendered_content = generate_error_page(api_endpoint, ERROR_COMMUNICATION_ENSEMBL)
        response_code = HTTPStatus.SERVICE_UNAVAILABLE

    return response_code, rendered_content


def fetch_karyotype(api_endpoint, params):
    api_resource = "/info/assembly"
    query_params = "content-type=application/json"
    species_name = quote(params["species"][0])
    api_url = f"{api_resource}/{species_name}?{query_params}"
    error_occurred, api_data = fetch_data_from_server(ENSEMBL_API_SERVER, api_url)
    if not error_occurred:
        karyotype_data = api_data["karyotype"]
        decoded_species_name = species_name.replace("%20", " ")
        context = {
            'species': decoded_species_name,
            'karyotype': karyotype_data
        }
        rendered_content = load_template("karyotype.html").render(context=context)
        response_code = HTTPStatus.OK
    else:
        rendered_content = generate_error_page(api_endpoint, ERROR_COMMUNICATION_ENSEMBL)
        response_code = HTTPStatus.SERVICE_UNAVAILABLE
    return response_code, rendered_content


def fetch_chromosome_length(api_endpoint, params):
    api_resource = "/info/assembly"
    query_params = "content-type=application/json"
    species_name = params["species"][0]
    chromosome_name = params["chromo"][0]
    api_url = f"{api_resource}/{species_name}?{query_params}"
    error_occurred, api_data = fetch_data_from_server(ENSEMBL_API_SERVER, api_url)
    if not error_occurred:
        chromosome_list = api_data["top_level_region"]
        chromosome_length = None
        for chromosome in chromosome_list:
            if chromosome['name'] == chromosome_name:
                chromosome_length = chromosome['length']
                break
        context = {
            'chromosome': chromosome_name,
            'length': chromosome_length
        }
        rendered_content = load_template("chromosome_length.html").render(context=context)
        response_code = HTTPStatus.OK
    else:
        rendered_content = generate_error_page(api_endpoint, ERROR_COMMUNICATION_ENSEMBL)
        response_code = HTTPStatus.SERVICE_UNAVAILABLE
    return response_code, rendered_content


def fetch_gene_id(gene_name):
    api_resource = f"/homology/symbol/human/{gene_name}"
    query_params = 'content-type=application/json;format=condensed'
    api_url = f"{api_resource}?{query_params}"
    error_occurred, api_data = fetch_data_from_server(ENSEMBL_API_SERVER, api_url)
    gene_identifier = None
    if not error_occurred:
        gene_identifier = api_data['data'][0]['id']
    return gene_identifier


def fetch_gene_sequence(params):
    api_endpoint = '/geneSeq'
    gene_name = params['gene'][0]
    gene_id = fetch_gene_id(gene_name)
    print(f"Gene: {gene_name} - Gene ID: {gene_id}")
    if gene_id:
        api_resource = "/sequence/id"
        query_params = "content-type=application/json"
        api_url = f"{api_resource}/{gene_id}?{query_params}"
        error_occurred, api_data = fetch_data_from_server(ENSEMBL_API_SERVER, api_url)
        if not error_occurred:
            gene_sequence = api_data['seq']
            context = {
                'gene': gene_name,
                'bases': gene_sequence
            }
            rendered_content = load_template("gene_seq.html").render(context=context)
            response_code = HTTPStatus.OK
        else:
            rendered_content = generate_error_page(api_endpoint, ERROR_COMMUNICATION_ENSEMBL)
            response_code = HTTPStatus.SERVICE_UNAVAILABLE
    else:
        rendered_content = generate_error_page(api_endpoint, ERROR_GENE_NOT_FOUND)
        response_code = HTTPStatus.NOT_FOUND
    return response_code, rendered_content


def fetch_gene_info(params):
    api_endpoint = '/geneInfo'
    gene_name = params['gene'][0]
    gene_id = fetch_gene_id(gene_name)
    print(f"Gene: {gene_name} - Gene ID: {gene_id}")

    if gene_id:
        api_resource = "/overlap/id"
        query_params = "content-type=application/json;feature=gene"
        api_url = f"{api_resource}/{gene_id}?{query_params}"
        error_occurred, api_data = fetch_data_from_server(ENSEMBL_API_SERVER, api_url)

        if not error_occurred:
            gene_data = api_data[0]
            gene_length = gene_data['end'] - gene_data['start']
            context = {
                'gene': gene_name,
                'start': gene_data['start'],
                'end': gene_data['end'],
                'length': gene_length,
                'id': gene_id,
                'chromosome_name': gene_data['assembly_name']
            }
            rendered_content = load_template("gene_info.html").render(context=context)
            response_code = HTTPStatus.OK
        else:
            rendered_content = generate_error_page(api_endpoint, ERROR_COMMUNICATION_ENSEMBL)
            response_code = HTTPStatus.SERVICE_UNAVAILABLE
    else:
        rendered_content = generate_error_page(api_endpoint, ERROR_GENE_NOT_FOUND)
        response_code = HTTPStatus.NOT_FOUND

    return response_code, rendered_content


def calculate_gene_bases(api_endpoint, params):
    gene_name = params["gene"][0]
    gene_id = fetch_gene_id(gene_name)
    print(f"Gene: {gene_name} - Gene ID: {gene_id}")

    if gene_id:
        api_resource = "/sequence/id"
        query_params = "content-type=application/json"
        api_url = f"{api_resource}/{gene_id}?{query_params}"
        error_occurred, api_data = fetch_data_from_server(ENSEMBL_API_SERVER, api_url)

        if not error_occurred:
            gene_sequence = api_data["seq"]
            base_counts = {"A": 0, "C": 0, "G": 0, "T": 0}
            for base in gene_sequence:
                if base in base_counts:
                    base_counts[base] += 1
            total_bases = sum(base_counts.values())
            base_percentages = {base: round((count / total_bases) * 100, 2) for base, count in base_counts.items()}
            context = {
                "gene": gene_name,
                "total_length": total_bases,
                "A": base_percentages["A"],
                "C": base_percentages["C"],
                "G": base_percentages["G"],
                "T": base_percentages["T"]
            }
            rendered_content = load_template("gene_calc.html").render(context=context)
            response_code = HTTPStatus.OK
        else:
            rendered_content = generate_error_page(api_endpoint, ERROR_COMMUNICATION_ENSEMBL)
            response_code = HTTPStatus.SERVICE_UNAVAILABLE
    else:
        rendered_content = generate_error_page(api_endpoint, ERROR_GENE_NOT_FOUND)
        response_code = HTTPStatus.NOT_FOUND

    return response_code, rendered_content


def fetch_gene_list(params):
    chromosome = params['chromo'][0]
    start = int(params['start'][0])
    end = int(params['end'][0])
    api_endpoint = f"/overlap/region/human/{chromosome}:{start}-{end}"
    query_params = "content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon"
    api_url = f"{api_endpoint}?{query_params}"
    error_occurred, api_data = fetch_data_from_server(ENSEMBL_API_SERVER, api_url)

    if not error_occurred:
        genes_list = [gene["external_name"] for gene in api_data if "external_name" in gene]
        context = {
            "chromo": chromosome,
            "start": start,
            "end": end,
            "gene_list": genes_list
        }
        rendered_content = load_template("gene_list.html").render(context=context)
        response_code = HTTPStatus.OK
    else:
        rendered_content = generate_error_page(api_endpoint, ERROR_COMMUNICATION_ENSEMBL)
        response_code = HTTPStatus.SERVICE_UNAVAILABLE

    return response_code, rendered_content


socketserver.TCPServer.allow_reuse_address = True

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        parsed_url = urlparse(self.path)
        api_endpoint = parsed_url.path
        params = parse_qs(parsed_url.query)

        print(f"Endpoint: {api_endpoint}")
        print(f"Parameters: {params}")

        response_code = HTTPStatus.OK
        content_type = "text/html"

        if api_endpoint == "/":
            file_path = os.path.join(HTML_FOLDER, "index.html")
            rendered_content = Path(file_path).read_text()
        elif api_endpoint == "/listSpecies":
            response_code, rendered_content = fetch_species_list(api_endpoint, params)
        elif api_endpoint == "/karyotype":
            response_code, rendered_content = fetch_karyotype(api_endpoint, params)
        elif api_endpoint == "/chromosomeLength":
            response_code, rendered_content = fetch_chromosome_length(api_endpoint, params)
        elif api_endpoint == "/geneSeq":
            response_code, rendered_content = fetch_gene_sequence(params)
        elif api_endpoint == "/geneInfo":
            response_code, rendered_content = fetch_gene_info(params)
        elif api_endpoint == "/geneCalc":
            response_code, rendered_content = calculate_gene_bases(api_endpoint, params)
        elif api_endpoint == "/geneList":
            response_code, rendered_content = fetch_gene_list(params)
        else:
            rendered_content = generate_error_page(api_endpoint, ERROR_RESOURCE_UNAVAILABLE)
            response_code = HTTPStatus.NOT_FOUND

        self.send_response(response_code)
        content_bytes = rendered_content.encode()
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content_bytes)))
        self.end_headers()

        self.wfile.write(content_bytes)

# Main program to start the server
with socketserver.TCPServer(("", SERVER_PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", SERVER_PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped by the user")
        httpd.server_close()