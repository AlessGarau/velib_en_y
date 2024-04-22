from flask import Flask, request, jsonify, session, make_response
from markupsafe import escape
import hashlib
from database_access_layer.database import connect_to_database
from database_access_layer.models.user import User
from mysql.connector.cursor import MySQLCursor
import json

app = Flask(__name__)
app.secret_key = b"4072bd90fe380021dd09cb1dc213a782b315656cf0e920866118ea0c2a3bf933"
cnx = connect_to_database()

def email_exists(email: str, cursor: MySQLCursor):
    """
    Function to check if an email already exists in db
    """
    query = ("SELECT email FROM `user` WHERE email = %s")
    cursor.execute(query, (email,))
    row = cursor.fetchall()

    return len(row) > 0

@app.route("/api/authentification/register/", methods=["POST"])
def register():
    data = request.get_json()
    user_firstname = str(escape(data.get("firstname")))
    user_lastname = str(escape(data.get("lastname")))
    user_email = str(escape(data.get("email")))
    user_password = str(hashlib.sha256(escape(data.get("password")).encode()).hexdigest())
    
    try:
        cursor = cnx.cursor(buffered=True)

        if not all((user_firstname, user_lastname, user_email, user_password)):
            raise BaseException('Credentials are not valid.')
        if email_exists(user_email, cursor):
            raise Exception('Email already exists.')

        query = ("INSERT INTO `user` (firstname, lastname, profile_picture, email, password) VALUES (%s,%s, '',%s,%s)")
        cursor.execute(query, (user_firstname, user_lastname, user_email, user_password,))

        cnx.commit()
        cursor.close()

        return jsonify({
            "data": cursor._last_insert_id,
            "success": True,
            "message": "User succesfully registered"
        }), 201
    
    except BaseException as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

@app.route('/api/authentification/login', methods=["POST"])
def login():
    data = request.get_json()
    user_email = str(escape(data.get("email")))
    user_password = str(hashlib.sha256(escape(data.get("password")).encode()).hexdigest())

    try:
        cursor = cnx.cursor(buffered=True)

        if not all((user_email, user_password)):
            raise BaseException("Credentials are not valid.")

        if  not email_exists(user_email, cursor):
            raise Exception("This email doesnt exist.")
        
        query = ("SELECT firstname, lastname , profile_picture, email, password FROM user WHERE email = %s")
        cursor.execute(query, (user_email,))
        rows = cursor.fetchone()
        user = User(*rows)

        if user_password != user.password:
            raise Exception("Email and password do not match.")
        
        session["user"] = json.dumps(user.to_dict())
        response = make_response(jsonify({
            "success": True,
            "message": "User successefully logged in."
            }))
        response.set_cookie('user', json.dumps(user.to_dict()))
        return response

    except BaseException as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

@app.route('/api/authentification/logout', methods=["GET"])
def logout():
    try:
        user_json = request.cookies.get('user')
        user = json.loads(user_json)
        user_session = session["user"]

        if not user:
            raise BaseException("No user cookies")
        
        if not user_session:
            raise BaseException("No user session")
        
        cursor = cnx.cursor(buffered=True)
        if not email_exists(user, cursor):
            raise BaseException("User does not exists.")
           
        response = make_response(jsonify({
            "message": "User successfully disconnected"
        }))

        response.delete_cookie("user")
        session.pop("user", None)
        return response
    
    except BaseException as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404

if __name__ == "__main__":
    app.run(debug=True)