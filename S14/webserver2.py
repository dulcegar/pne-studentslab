#nos pide implementar nuestro propio handler, crearnos nosotros el nuestro

import http.server
import socketserver

# Define the Server's port
PORT = 8080


# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inherits all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler): #esto es lo nuevo, creamos una clase personalizada para atender a las necesidades en nuestro http
#testhandler es una clase hija de basehttprequesthandler
#de la de simplehttprequest handler no la podemos adaptar, la de base... si
    def do_GET(self):  #indicamos que hacer cuando recibimos una peticion del tipo GET
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # We just print a message
        print("GET received!")

        # IN this simple server version:
        # We are NOT processing the client's request
        # We are NOT generating any response message
        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler #almacenamos en la variable Handler la clase nuestra que hemos creado en vez de una de las que ya existen en python como hemos hecho en la version 1
#almacenamos una clase de handler personalizada

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_clo