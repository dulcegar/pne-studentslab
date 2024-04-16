import http.server
import socketserver
import termcolor

# Define the Server's port
PORT = 8080   #para probarlo hay q poner 127.0.0.1:8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inherits all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # IN this simple server version:
        # We are NOT processing the client's request
        # It is a happy server: It always returns a message saying
        # that everything is ok

        # Message to send back to the client
        contents = "I am the happy server! :-)"

        # Generating the response message
        self.send_response(200)  # -- Status line: OK!
        #es una herramienta que ya vienne en el basehttprequestserver
        #el 200 significa tdo okay, yo puedo adarptar el numero q le paso al self response
        #el self_response ya sabe que mensaje tiene dependiendo del numero que le mando
        #con esto añadimos la status line ( no tenemos q hacer lo q en otras hemos hecho)

        # Define the content-type header:
        self.send_header('Content-Type', 'text/plain') #send_header es otro metodo de la clase base...
        self.send_header('Content-Length', len(contents.encode()))  #lo encode en bytes y lo manda para poner la length
        #para seguir mandando funciones tendriamos que seguir llamando al send_header

        # The header is finished
        self.end_headers()  #añade la linea en blanco para separar tdo lo de la cabecera

        # Send the response message
        self.wfile.write(contents.encode()) #envia de vuelta el contenido encoded en bytes
        #el wfile significa Write file (fichero de escritura)
        #wfile es el sentido que va del servidor al cliente
        #con rfile es el fichero de lectura

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()