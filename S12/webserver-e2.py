import socket
import termcolor

IP = "127.0.0.1"
PORT = 8080


def process_client(client_socket):
    request_bytes = client_socket.recv(2048)
    request = request_bytes.decode()
    print("Message FROM CLIENT: ")
    lines = request.splitlines()
    request_line = lines[0]
    print("Request line: ", end="")
    termcolor.cprint(request_line, 'green')

    body = """
    <!DOCTYPE html>
    <html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <title>Green server</title>
      </head>
      <body style="background-color: lightgreen;">
        <h1>GREEN SERVER</h1>
        <p>I am the Green Server! :-)</p>
      </body>
    </html>
    """
    status_line = "HTTP/1.1 200 OK\n"
    header = "Content-Type: text/plain\n"
    header += f"Content-Length: {len(body)}\n"
    response = f"{status_line}{header}\n{body}"
    response_bytes = response.encode()
    client_socket.send(response_bytes)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

print("SEQ Server configured!")

try:
    while True:
        print("Waiting for clients....")

        (client_socket, client_address) = server_socket.accept()
        process_client(client_socket)
        client_socket.close()
except KeyboardInterrupt:
    print("Server Stopped!")
    server_socket.close()
