import json
from flask import request


def get_user_from_cookie() -> dict | None:
    user_json = request.cookies.get("user")
    user = json.loads(user_json) if user_json else None

    return user
