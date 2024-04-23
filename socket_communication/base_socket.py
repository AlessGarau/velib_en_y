import socket
import json

class Socket:

    def __init__(self, port):
        self.host = socket.gethostname()
        self.port = port
        self.message_start_length = 10

    def create_socket(self):
        self.socket = socket.socket()

    def _raw_send(_, socket, message):
        payload = f"{len(message)}:{message}"
        socket.send(payload.encode())

    def _raw_send_json(self, socket, data):
        json_data = json.dumps(data)
        self._raw_send(socket, json_data)

    def _raw_receive(self, socket):
        received_bytes = socket.recv(self.message_start_length)
        received_data_start = received_bytes.decode("utf-8")

        size, *message = received_data_start.split(":")
        size = int(size)
        message = ":".join(message)
        print(message)

        if size > len(message):
            remaining_bytes = socket.recv(size - len(message))
            message += remaining_bytes.decode("utf-8")

        return message

    def _raw_receive_json(self, socket):
        raw_data = self._raw_receive(socket)
        json_data = json.loads(raw_data)
        return json_data