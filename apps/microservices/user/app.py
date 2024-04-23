import json
import hashlib

from flask import Flask, request, jsonify
from mysql.connector.cursor import MySQLCursor

from database_access_layer.database import close_connection, connect_to_database
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


@app.route("/api/users", methods=['GET'])
def user_profile():
    cnx = connect_to_database()

    user_json = request.cookies.get('user')
    user = json.loads(user_json) if user_json else None

    try:
        cursor = cnx.cursor(buffered=True)

        if not (user and user_exists(user["id"], cursor)):
            raise BaseException("Credentials are not valid. Check the user's validity.")
        select_query = """
            SELECT *
            FROM user
            WHERE user_id=%s
        """

        cursor.execute(select_query, (user["id"],))
        user = User(*cursor.fetchone())
        cursor.close()

        return jsonify({
            'data': user.to_dict(),
            'success': True
        }), 200

    except BaseException as e:
        return jsonify({
            'message': str(e),
            'success': False
        }), 400
    finally:
        close_connection(cnx)


@app.route("/api/users", methods=['PUT'])
def update_user():
    cnx = connect_to_database()

    body = request.get_json()
    type = request.args.get("type")
    user_json = request.cookies.get('user')
    user = json.loads(user_json) if user_json else None

    try:
        cursor = cnx.cursor(buffered=True)

        if not (user and user_exists(user["id"], cursor)):
            raise BaseException("Credentials are not valid. Check the user's validity.")
        user_id = user["id"]

        match type:
            case "password":
                password = body.get("password")

                if not password:
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
                    'data': None,
                    'success': True
                }), 204
            case "profile":
                firstname = body.get('firstname')
                lastname = body.get('lastname')
                profile_picture = body.get('profile_picture') if body.get('profile_picture') else ""

                if not all((firstname, lastname)):
                    raise BaseException("Credentials are not valid.")

                update_query = """
                    UPDATE user
                    SET firstname = %s, lastname = %s,  profile_picture = %s
                    WHERE user_id = %s
                """
                cursor.execute(update_query, (firstname, lastname, profile_picture, user_id,))
                cnx.commit()

                select_query = """
                    SELECT *
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
            case _:
                return jsonify(
                    {
                        "success": False,
                        "message": f'The type of update "{type}" is not known'
                    }
                ), 404
    except BaseException as e:
        return jsonify({
            'message': str(e),
            'success': False
        }), 400
    finally:
        close_connection(cnx)


@app.route("/api/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    cnx = connect_to_database()

    user_json = request.cookies.get('user')
    user = json.loads(user_json) if user_json else None

    try:
        cursor = cnx.cursor(buffered=True)

        if not (user and user_exists(user["id"], cursor) and user_id != user["id"]):
            raise BaseException("Credentials are not valid. Check the user's validity.")

        delete_query = """
            DELETE FROM user 
            WHERE user_id = %s
        """
        cursor.execute(delete_query, (user["id"],))
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
    finally:
        close_connection(cnx)


if __name__ == '__main__':
    app.run()
