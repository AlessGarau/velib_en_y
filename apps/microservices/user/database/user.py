import hashlib
from .request import Request

class User:
    def __init__(self):
        self.request = Request()

    def to_hash(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def get_by_id(self, user_id):
        user_data, *_ = self.request.select("SELECT firstname, lastname, profile_picture, email FROM user WHERE user_id = ?", (user_id,))
        return user_data

    def update_profile(self, user_id, data):
        """
        data = {
            "firstname": str,
            "lastname": str,
            "profile_picture": str,
            "email": str,
        }
        """
        self.request.update(
            "UPDATE user SET firstname = ?, lastname = ?, profile_picture = ?, email = ? WHERE user_id = ?",
            (data.get("firstname"), data.get("lastname"), data.get("profile_picture"), data.get("email"), user_id)
        )
        return {
            "status": "success",
            "message": "Updated user profile"
        }

    def update_password(self, user_id, password):
        password_hash = self.to_hash(password)
        self.request.update(
            "UPDATE user SET password = ? WHERE user_id = ?", (password_hash, user_id)
        )
        return {
            "status": "success",
            "message": "Updated user password"
        }

    def delete(self, user_id):
        self.request.delete(
            "DELETE FROM user WHERE user_id = ?", (user_id)
        )
        return {
            "status": "success",
            "message": "Deleted user"
        }