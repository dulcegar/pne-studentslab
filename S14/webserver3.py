import http.server
import socketserver
import termcolor #nos pide que pintemos mensajes con color

# Define the Server's port
PORT = 8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inherits all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):   #en este nos cambia el contenido del do_GET
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # We just print a message
        print("GET received! Request line:")

        # Print the request line
        termcolor.cprint("  " + self.requestline, 'green')
        #el requestlines es un atributo que viene del base (esta hai declarado por python), por lo q lo heredamos y podemos utilizarlo

        # Print the command received (should be GET)
        print("  Command: " + self.command) #pintamos el metodo/comando (que es GET)

        # Print the resource requested (the path)
        print("  Path: " + self.path) #pintamos el path (la ruta)

        # IN this simple server version:
        # We are NOT processing the client's request
        # We are NOT generating any response message
        return


# ------------------------
# - Server MAIN program    #no cambia, lo mismo q en los tres
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
        print("Stopped by the user")
        httpd.server_close()