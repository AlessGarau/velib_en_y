from flask import Flask, request, jsonify
from database.user import User
from database.database_error import DatabaseConnectionError, DatabaseQueryError
import re #regex

app = Flask(__name__)
user = User()

@app.get("/api/user")
def index():
    # Authorization with Auth Microservice
    # If not authorized, return Error 401
    # Else retrieve user_id
    user_id=1

    return jsonify(user.get_by_id(user_id)), 200

@app.patch("/api/user/update/<str:type>")
def update(type):
    # Authorization with Auth Microservice
    # If not authorized, return Error 401
    # Else retrieve user_id

    match type:

        # Update password (/api/user/update?type="password")
        case "password":
            if ("password" not in request.json["password"]):
                return jsonify(
                    {
                        "status": "failed",
                        "message": "Wrong request body format"
                    }
                ), 400
            return jsonify(user.update_password(user_id, request.json["password"])), 200

        # Update profile
        case "profile":
            # Check request body data format
            if ("firstname" not in request.json["firstname"] or not isinstance(request.json["firstname"], str) or len(request.json["firstname"]) == 0
                    or "lastname" not in request.json["lastname"] or not isinstance(request.json["lastname"], str) or len(request.json["lastname"]) == 0
                    or "mail" not in request.json["mail"] or not isinstance(request.json["mail"], str) or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', request.json["mail"])):
                return jsonify(
                    {
                        "message": "Wrong request body format"
                    }
                ), 400
            return jsonify(user.update_profile(user_id, request.json)), 200

        case _:
            return jsonify(
                {
                    "status": "failed",
                    "message": f'The type of update "{type}" is not known'
                }
            ), 404

@app.delete("/api/user/delete")
def delete():
    # Authorization with Auth Microservice
    # If not authorized, return Error 401
    # Else retrieve user_id

    return jsonify(user.delete(user_id)), 200

@app.errorhandler(DatabaseConnectionError)
def handle_database_connection_error(e):
    return jsonify(
        {
            "status": "failed",
            "message": f"Connection to database failed : {e}"
        }
    ), 500

@app.errorhandler(DatabaseQueryError)
def handle_database_query_error(e):
    return jsonify(
        {
            "status": "failed",
            "message": f"Database query failed : {e}"
        }
    ), 500