from .base_socket import Socket

class ClientSocket(Socket):
    def __init__(self, port):
        super().__init__(port)

    def connect(self):
        self.create_socket()
        self.socket.connect((self.host, self.port))

    def read(self):
        self.connect()
        response = super()._raw_receive_json(self.socket)
        self.disconnect()
        return response

    def disconnect(self):
        self.socket.shutdown(2)
        self.socket.close()
        del self.socket