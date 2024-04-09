import http.server
import socketserver

# Define the Server's port
PORT = 8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True  #indica que vamos a utilizar el puerto

# -- Use the http.server Handler
handler = http.server.SimpleHTTPRequestHandler #handler = manejador/gestor, almacenamos dentro de una variable cual va a ser el nombre de la clase del objeto que se va a encargar de atender las peticiones http de nuestro servidor
#el simplehhtrequesthandler esta ya creado en la variable http.server

# -- Open the socket server
with socketserver.TCPServer(("", PORT), handler) as httpd:  #poniendo "" nos c0ge por defecto la ip local, por eso no la ponemos arriba
#se crea el spcket del servidor, TPCServer es una clase del modulo socketserver. Estamos llamando al constructor de la clase TPCServer y le estamos pasando la dirrecion del servir(ip,port) y la variable handler que tenia el simplehttp.

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server Stopped!")
        httpd.server_close()
