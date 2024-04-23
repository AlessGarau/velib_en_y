from flask import Flask, request, jsonify
from mysql.connector.cursor import MySQLCursor
import hashlib

from database_access_layer.database import connect_to_database
from database_access_layer.models.user import User

app = Flask(__name__)
cnx = connect_to_database()

def user_exists(user_id: int, cursor: MySQLCursor) -> bool:
    """
    Checks that the user targeted (user_id) exists in the db
    """
    select_query = """
        SELECT * 
        FROM user 
        WHERE user_id=%s
    """
    cursor.execute(select_query, (user_id,))
    user = cursor.fetchall()

    return len(user) > 0

def to_hash(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

@app.get("/api/user")
def user_profile():
    body = request.get_json()
    user_id = body.get('user_id')

    try:
        cursor = cnx.cursor(buffered=True)
        select_query = """
            SELECT *
            FROM user
            WHERE user_id=%s
        """

        cursor.execute(select_query, (user_id,))
        user = cursor.fetchone()
        cursor.close()

        return jsonify({
            'data': user,
            'success': True
        }), 200
    
    except BaseException as e:
        return jsonify({
            'message': str(e),
            'success': False
        }), 400

@app.patch("/api/user/update/<string:type>")
def update_user(type):
    body = request.get_json()
    user_id = body.get('user_id')

    if not user_exists(user_id, cursor):
        raise BaseException(f"Favorite station {user_id} doesn't exists")
    
    match type:

        # Update password (/api/user/update/password)
        case "password":

            password = body.get('password')
            
            try:
                cursor = cnx.cursor(buffered=True)

                if not password :
                    raise BaseException("Credentials are not valid.")
                
                update_query = """
                    UPDATE user
                    SET password = %s
                    WHERE user_id = %s
                """
                cursor.execute(update_query, (to_hash(password), user_id,))
                cnx.commit()

                cursor.close()

                return jsonify({
                    'data': {
                        'new_password' : password
                    },
                    'success': True
                }), 200
            
            except BaseException as e:
                return jsonify({
                    'message': str(e),
                    'success': False
                }), 400

        # Update profile (/api/user/update/profile)
        case "profile":
            firstname = body.get('firstname')
            lastname = body.get('lastname')
            profile_picture = body.get('profile_picture')
            email = body.get('email')
            
            try:
                cursor = cnx.cursor(buffered=True)

                if not all((firstname, lastname, email)) :
                    raise BaseException("Credentials are not valid.")
                
                update_query = """
                    UPDATE user
                    SET firstname = %s, lastname = %s,  profile_picture = %s, email = %s
                    WHERE user_id = %s
                """
                cursor.execute(update_query, (firstname, lastname, profile_picture, email, user_id,))
                cnx.commit()

                select_query = """
                    SELECT firstname, lastname, profile_picture, email
                    FROM user
                    WHERE user_id = %s
                """
                cursor.execute(select_query, (user_id,))
                updated_user = User(*cursor.fetchone())

                cursor.close()

                return jsonify({
                    'data': updated_user.to_dict(),
                    'success': True
                }), 200
            
            except BaseException as e:
                return jsonify({
                    'message': str(e),
                    'success': False
                }), 400

        case _:
            return jsonify(
                {
                    "success": "failed",
                    "message": f'The type of update "{type}" is not known'
                }
            ), 404

@app.delete("/api/user/delete")
def delete():
    body = request.get_json()
    user_id = body.get('user_id')

    try:
        cursor = cnx.cursor(buffered=True)

        if not user_exists(user_id, cursor):
            raise BaseException("Credentials are not valid. Check the user's validity.")

        delete_query = """
            DELETE FROM user 
            WHERE user_id = %s
        """
        cursor.execute(delete_query, (user_id,))
        cnx.commit()
        cursor.close()

        return jsonify({
            'data': None,
            'success': True
        }), 204
    
    except BaseException as e:
        return jsonify({
            'message': str(e),
            'success': False
        }), 400

if __name__ == '__main__':
    app.run()