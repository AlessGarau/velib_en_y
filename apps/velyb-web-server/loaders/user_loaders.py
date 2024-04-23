import json
from flask import request


def get_user_from_cookie() -> dict | None:
    # Pour tester la vue User / Invité, commenter soit A soit B

    # A - Cookie, session
    # user_json = request.cookies.get("user")
    # user = json.loads(user_json) if user_json else None

    # B - Hard coded
    user = {
        "email": "m@m.com",
        "firstname": "Flash",
        "id": 16,
        "lastname": "McQueen",
        "profile_picture": "https://static.fnac-static.com/multimedia/Images/DD/DD/20/B5/11870429-1505-1505-1/tsp20200306111033/Poster-Cars-Characters-91-5x61cm.jpg"
    }
    return user
