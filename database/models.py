class FavoriteStation:
    def __init__(self, station_code, user_id, name, picture=None, name_custom=None) -> None:
        self.station_code = station_code
        self.user_id = user_id
        self.name = name
        self.picture = picture
        self.name_custom = name_custom
