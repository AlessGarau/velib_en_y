import json
import socket
from abc import ABC, abstractmethod
import time

from cache_protocol_models.request import Request
from cache_protocol_models.response import Response


class CacheProtocol(ABC):
    # Base values
    API_URL = ""
    DELAY = 0
    CACHE_START_TIME = 0
    CACHE = ""

    def __init__(self, ADDRESS_HOST, PORT_DEFAULT, endpoint_to_cache: str, delay: int) -> None:
        self.__HOST = ADDRESS_HOST
        self.__PORT = PORT_DEFAULT
        self.API_URL = endpoint_to_cache
        self.DELAY = delay
        self.routes = {}

        self.__set_socket()
        self.__launch_server()

    def __launch_server(self):
        print(f"Server running on port {self.__PORT}")
        try:
            while True:
                client, address = self.server_socket.accept()
                request = Request(client.recv(1024).decode())
                response = Response(client)

                if not self.check_path(request.path):
                    response.make_response(data=json.dumps({'message': "This route doesn't exist"}), code=404)
                elif not request.method in self.routes[request.path]:
                    response.make_response(code=500)
                elif request.method in self.routes.values():
                    if not self.get_cache_validity():
                        self.set_cache()
                    print(self.get_cache())
                    response.make_response(data="self.get_cache()", code=200)
                else:
                    response.make_response(code=500)

                # print(f"New connection: {address}") ajouter methode, reponse etc
                response.send_response()
        except KeyboardInterrupt:
            print("Server is shutting down...")
        finally:
            self.server_socket.close()
            print("Server is down")

    def __set_socket(self) -> None:
        self.server_socket = socket.create_server((self.__HOST, self.__PORT), reuse_port=True)

    def check_path(self, path: str) -> bool:
        return path in self.routes.keys()

    def set_route(self, route_path: str, accepted_methods: list) -> None:
        self.routes[route_path] = accepted_methods

    def set_cache_start(self, time: float):
        self.CACHE_START_TIME = time

    def get_cache_validity(self):
        current_time = time.time()
        if current_time - self.CACHE_START_TIME > self.DELAY:
            self.set_cache_start(current_time)
            return True
        else:
            return False

    def get_cache(self) -> str:
        return self.CACHE

    @abstractmethod
    def set_cache(self):
        pass
