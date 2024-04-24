import json
import requests
import os

from cache_protocol_models.cache_protocol import CacheProtocol

ADDRESS_HOST = os.getenv('TCP_HOST')
PORT_DEFAULT = int(os.getenv('TCP_PORT'))


class OpenDataCache(CacheProtocol):
    VELIB_COUNT = 0

    def __init__(self, ADDRESS_HOST, PORT_DEFAULT, endpoint_to_cache: str, delay: int) -> None:
        super().__init__(ADDRESS_HOST, PORT_DEFAULT, endpoint_to_cache, delay)

    def set_cache(self) -> None:
        res = requests.get(self.API_URL).json()
        self.VELIB_COUNT = res.get('total_count')
        offset = self.VELIB_COUNT

        while (offset >= 100):
            next_res = requests.get(self.API_URL + f"&offset={self.VELIB_COUNT - offset if offset > 200 else offset}").json()
            res["results"].extend(next_res["results"])
            offset -= 100

        self.CACHE = json.dumps(res)


if __name__ == "__main__":
    server = OpenDataCache(ADDRESS_HOST,
                           PORT_DEFAULT,
                           "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=100",
                           300)

    server.set_route('/', "GET")
    server.start()
