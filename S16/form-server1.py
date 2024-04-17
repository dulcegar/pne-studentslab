import http.server
import socketserver
import termcolor
from pathlib import Path
import os

PORT = 8080
HTML_FOLDER = "html" #esto es una constante que determina donde tengo la carpeta con tdo el contenido html para que luego en vez de cambiar tds si quiero pues solo cambiar la constante

socketserver.TCPServer.allow_reuse_address = True


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self): #independientemente de lo q pida el cliente, siempre manda un 200 (ok)
        termcolor.cprint(self.requestline, 'green')

        #contents = Path(f'{HTML_FOLDER}/form-1.html').read_text() asi puesto no sirve para windows xqe ahi se separa con \ en vez de /, para que funcione con todo usamos el os.path.join
        file_path = os.path.join(HTML_FOLDER, "form-1.html")
        contents = Path(file_path).read_text()

        self.send_response(200)

        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', f"{len(str.encode(contents))}")
        self.end_headers()

        self.wfile.write(str.encode(contents)) #para enviar al cliente la respuesta

        return


with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
    print("Serving at PORT", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()