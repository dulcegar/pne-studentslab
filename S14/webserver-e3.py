import http.server
import socketserver
import termcolor
from pathlib import Path

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        if self.path == "/" or self.path == "/index.html":
            contents = Path("index.html").read_text()
            self.send_response(200)
        else:
            resource = self.path[1:] # path seria "/myfile.html" y con los [1:] me estoy quedando con "myfile.html"
            try:
                contents = Path(f"{resource}").read_text() #si existe me guardo aqui el contenido
                self.send_response(200) #esto lo tenemos que poner xqe solo tiene sentido que se ejecute si lo de arriba esta bn, sino salta al error
            except FileNotFoundError: #si intento abrir el fichero y no existe me saltaria esto
                contents = Path(f"error.html").read_text()
                self.send_response(404)

        contents_bytes = contents.encode()
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)

        return


with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT...", PORT)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()