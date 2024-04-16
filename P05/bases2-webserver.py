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
        if resource == "/" or resource == "/index.html":
            file_name = os.path.join("html", "index.html")
            body = Path(file_name).read_text()
            self.send_response(200)

        elif resource == "/info/A.html":
            file_name = os.path.join("html", "info", "A.html")
            body = Path(file_name).read_text()  # el Path es una clase que esta dentro del modulo pathlib. Nos estamos creando un objeto de la clase Path, es la llamda al constructor. Llamos al metodo con read_text y me lee tdo el fichero A.html.
            self.send_response(200)

        elif resource == "/info/C.html":   #basicamente en cada if/elif genera la ruta al fichero que tiene que abrir
            file_name = os.path.join("html", "info", "C.html")
            body = Path(file_name).read_text()
            self.send_response(200)

        elif resource == "/info/G.html":
            file_name = os.path.join("html", "info", "G.html")
            body = Path(file_name).read_text()
            self.send_response(200)

        elif resource == "/info/T.html":
            file_name = os.path.join("html", "info", "T.html")
            body = Path(file_name).read_text()
            self.send_response(200)

        else:
            resource = self.path[1:]
            try:
                file_name = os.path.join("html", resource)
                body = Path(file_name).read_text()  # si existe me guardo aqui el contenido
                self.send_response(200)
            except FileNotFoundError:
                file_name = os.path.join("html", "error.html")
                body = Path(file_name).read_text()
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