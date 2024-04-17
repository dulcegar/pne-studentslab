import http.server
import socketserver
import termcolor
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import jinja2 as j
import os


def read_html_file(filename):
    contents = Path("html/" + filename).read_text()
    contents = j.Template(contents)
    return contents


PORT = 8080
HTML_FOLDER = "html"

socketserver.TCPServer.allow_reuse_address = True


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')

        url_path = urlparse(self.path)
        path = url_path.path
        print(f"Path: {path}")
        arguments = parse_qs(url_path.query)
        print(f"Arguments: {arguments}")
        if path == "/":
            file_path = os.path.join(HTML_FOLDER, "form-e2.html")
            contents = Path(file_path).read_text()
            self.send_response(200)
        elif path == "/echo":
            try:
                msg_param = arguments['msg'][0]
                context = {     #nos creamos un diccionario con dos parejas clace-valor
                    'capital_letters': 'capital_letters' in arguments,
                    'todisplay': msg_param
                }    #esta variable es para meterla luego en el context y no meterla a cascoporro
                contents = read_html_file("result-echo-server-e2.html").render(context=context) #el context rojo es un parametro y el blanco es nuestra variable

                #si no tuviesemos jinja
                # contents = """
                #     <!DOCTYPE html>
                #     <html lang="en">
                #         <head>
                #             <meta charset="utf-8">
                #             <title>Result</title>
                #         </head>
                #         <body>
                #             <h1>Echoing the receiving message:</h1>
                #     """
                # if 'capital_letters' in arguments:
                #     contents += f"<p>{msg_param.upper()}</p>"
                # else:
                #     contents += f"<p>{msg_param}</p>"
                # contents += """
                #             <a href="/">Main page</a>
                #         </body>
                #     </html>"""
                self.send_response(200)
            except (KeyError, IndexError):
                file_path = os.path.join(HTML_FOLDER, "error.html")
                contents = Path(file_path).read_text()
                self.send_response(404)
        else:
            file_path = os.path.join(HTML_FOLDER, "error.html")
            contents = Path(file_path).read_text()
            self.send_response(404)

        contents_bytes = contents.encode()
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(contents_bytes)))
        self.end_headers()

        self.wfile.write(contents_bytes)


with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("Serving at PORT...", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Stopped by the user")
        httpd.server_close()