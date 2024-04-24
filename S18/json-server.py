import http.server
import socketserver
import termcolor
from pathlib import Path
import jinja2 as j
from urllib.parse import urlparse, parse_qs

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True


def read_html_file(filename):
    contents = Path(filename).read_text()
    contents = j.Template(contents)
    return contents


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        parsed_url = urlparse(self.path)
        path = parsed_url.path
        params = parse_qs(parsed_url.query)
        print(path, params)

        #AQUI ES DONDE EMPIEZA LO DIFERENTE
        if path == "/":
            contents = read_html_file("index.html").render()  #lo renderiza pero no le manda contexto porq no tiene nada q sustituir ,,,, si no tenemos el read_html_filr se usaria el Path...
            content_type = 'text/html' #para mandarle la respuesta al cliente, indique que tipo es
            status_code = 200
        elif path == "/listusers":  #comn /listuser no se trabaja con html, lee el fichero de json y le manda application/json
            contents = Path('people-3.json').read_text()
            content_type = 'application/json'  #dependiendo del recurso que el cliente solicite va a contestar con un contenido y un tipo de contenido
            status_code = 200
        else:
            contents = Path("error.html").read_text()
            content_type = 'text/html'
            status_code = 404

        contents_bytes = contents.encode()
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)

        return


with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()