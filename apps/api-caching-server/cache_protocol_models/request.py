class Request:

    def __init__(self, request: str) -> None:
        self.request = request
        self.headers = dict()
        self.method = ""
        self.path = ""

        self.parse_req()

    def parse_req(self):
        lines = self.request.split("\r\n")
        start_line = lines[0]

        # TODO HEADER

        self.method, self.path, _ = start_line.split(" ")
