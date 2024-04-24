class Request:

    def __init__(self, request: str) -> None:
        self.request = request
        self.headers = ""
        self.method = ""
        self.path = ""

        self.parse_req()

    def parse_req(self):
        lines = self.request.split('\r\n')
        start_line = lines[0]

        self.headers = lines[1:]
        self.method, self.path, _ = start_line.split(' ')

    def get_origin_header(self) -> str | None:
        for header in self.headers:
            if (header.startswith('Origin: ')):
                return header.removeprefix('Origin: ')
