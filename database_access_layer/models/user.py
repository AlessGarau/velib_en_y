from .abstract import AbstractModel


class User(AbstractModel):
    def __init__(self, id: str, firstname: str, lastname: str, profile_picture: str, email: str, password: str) -> None:
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.profile_picture = profile_picture
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'profile_picture': self.profile_picture,
            'email': self.email,
        }
