class Client:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

    def ping(self):
        print("Ok!")

    def __str__(self):
        print(f"Connection to SERVER at {self.IP}, PORT: {self.PORT}")
        return self.IP and self.PORT

