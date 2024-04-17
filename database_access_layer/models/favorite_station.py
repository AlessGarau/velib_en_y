from .abstract import AbstractModel


class FavoriteStation(AbstractModel):
    def __init__(self, station_code: str, user_id: int, name: str, picture: str = None, name_custom: str = None) -> None:
        self.station_code = station_code
        self.user_id = user_id
        self.name = name
        self.picture = picture
        self.name_custom = name_custom

    def to_dict(self):
        return {
            'station_code': self.station_code,
            'user_id': self.user_id,
            'name': self.name,
            'picture': self.picture,
            'name_custom': self.name_custom
        }
