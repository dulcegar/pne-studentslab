import http.server
import socketserver
import termcolor
from pathlib import Path #lo importamos para trabajar cn las rutas

PORT = 8080

socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        if self.path == "/" or self.path == "/index.html":
            contents = Path("index.html").read_text() #ahora almacenamos el contenido de una pagina web
            self.send_response(200) #ok
        else:
            contents = Path("error.html").read_text()
            self.send_response(404) #error

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