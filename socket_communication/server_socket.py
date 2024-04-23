from .base_socket import Socket

class ServerSocket(Socket):
    def __init__(self, port):
        super().__init__(port)
        self.create_socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

    def accept(self):
        client, address = self.socket.accept()
        print(f"[log] Connection from {address}")
        self.client = client

    # Not used
    def send(self, message):
        if not self.__valid_client():
            return
        super()._raw_send(self.client, message)

    def send_json(self, json_data):
        if not self.__valid_client():
            return
        super()._raw_send_json(self.client, json_data)


    def close_client(self):
        if not self.__valid_client():
            return
        self.client.close()
        del self.client

    def __valid_client(self):
        try:
            _ = self.client
            return True
        except:
            print("[ERROR] No client connection")
            return False