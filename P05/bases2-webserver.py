import http.server
import socketserver
import termcolor
from pathlib import Path
import os

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True


class myHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        resource = self.path

        #nos creamos un diccionario para transformar un recurso en el fichero correspondiente y para resumir tdo el codigo:
        resource_to_file = {
            "/": "index.html",
            "/index.html": "index.html",
            "/info/A.html": os.path.join("info", "A.html"),
            "/info/C.html": os.path.join("info", "C.html"),
            "/info/G.html": os.path.join("info", "G.html"),
            "/info/T.html": os.path.join("info", "T.html"),
        }

        file_name = resource_to_file.get(resource, resource[1:]) #la segunda variable entre los () es lo que devolveriamos a file_name gracias al get y a no ponerlo entre []
        file_path = os.path.join("html", file_name) #le añadimos html a el file_name al que hemos quitado la barra de alante

        try:
            body = Path(file_path).read_text()  # si existe me guardo aqui el contenido
            self.send_response(200)
        except FileNotFoundError:
            file_path = os.path.join("html", "error.html")
            body = Path(file_path).read_text()
            self.send_response(404)

        body_bytes = body.encode()
        self.send_header('Content-Type', 'text/html')  # como ahora siempre trabajamos con html ponemos text/html.
        self.send_header('Content-Length', str(len(body_bytes)))
        self.end_headers()

        self.wfile.write(body_bytes)

        return


with socketserver.TCPServer(("", PORT), myHandler) as httpd:
    print("Serving at PORT...", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()
