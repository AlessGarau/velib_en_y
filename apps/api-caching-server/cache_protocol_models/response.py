import socket


class Response:
    def __init__(self, client: socket, data: str = "", code: int = 200, content_type: str = 'application/json', origin: str = None) -> None:
        self.__SEPARATOR = "\r\n"
        self.__HTTP = {
            200: "HTTP/1.1 200 OK",
            300: "HTTP/1.1 300 Forbidden",
            404: "HTTP/1.1 404 NOT FOUND",
            500: "HTTP/1.1 500 Internal server error"
        }
        self.__CONTENT_TYPE = content_type
        self.client = client
        self.data = data
        self.code = code
        self.origin = origin

    def make_response(self, data: str = "", code: int = 200) -> None:
        self.data = data
        self.code = code

    def send_response(self) -> None:
        response = ""
        match self.code:
            case 404 | 200:
                response += f"{self.__HTTP[self.code]}{self.__SEPARATOR}"
                response += f"Access-Control-Allow-Origin: {self.origin}{self.__SEPARATOR}"
                response += f"Content-Type: {self.__CONTENT_TYPE}{self.__SEPARATOR}"
                response += f'Content-Length: {len(self.data)}{self.__SEPARATOR}{self.__SEPARATOR}'
                response += f"{self.data}{self.__SEPARATOR}"
            case 300:
                response += f"{self.__HTTP[self.code]}{self.__SEPARATOR}"
            case _:
                response += self.__HTTP[500]

        try:
            self.client.send(response.encode())
        except Exception as e:
            print(f"Error sending response: {e}")
        finally:
            self.client.close()
