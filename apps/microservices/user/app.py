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

    body = request.get_json()
    user_id = body.get('user_id')

    try:
        cursor = cnx.cursor(buffered=True)

        if not user_exists(user_id, cursor):
            raise BaseException("Cet utilisateur n'existe pas.")
        select_query = """
            SELECT *
            FROM user
            WHERE user_id=%s
        """

        cursor.execute(select_query, (user_id,))
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


@app.route("/api/users", methods=['POST'])
def update_user():
    cnx = connect_to_database()

    body = request.get_json()
    user_id = body.get('user_id')
    type = request.args.get("type")

    try:
        cursor = cnx.cursor(buffered=True)

        if not user_exists(user_id, cursor):
            raise BaseException("Cet utilisateur n'existe pas.")

        match type:
            case "password":
                new_password = body.get("new_password")
                new_password_repeated = body.get("new_password_repeated")
                old_password = body.get("old_password")

                if not all((new_password, new_password_repeated, old_password)):
                    raise BaseException("Veuillez remplir l'intégralité des champs.")

                if new_password != new_password_repeated:
                    raise BaseException("Le nouveau mot de passe et sa vérification ne correspondent pas.")

                hashed_old_password = to_hash(old_password)
                select_user = """
                    SELECT * 
                    FROM user
                    WHERE user_id = %s AND password = %s
                """
                cursor.execute(select_user, (user_id, hashed_old_password))
                rows = cursor.fetchall()

                if len(rows) == 0:
                    raise BaseException("Ancien mot de passe incorrecte. Veuillez réessayer.")

                hashed_new_password = to_hash(new_password)
                update_query = """
                    UPDATE user
                    SET password = %s
                    WHERE user_id = %s
                """
                cursor.execute(update_query, (hashed_new_password, user_id))
                cnx.commit()

                cursor.close()

                return jsonify({
                    'message': "Mot de passe modifié avec succès.",
                    'success': True
                }), 200
            case "profile":
                firstname = body.get('firstname')
                lastname = body.get('lastname')
                profile_picture = body.get('profile_picture') if body.get('profile_picture') else ""

                if not all((firstname, lastname)):
                    raise BaseException("Veuillez remplir l'intégralité des champs.")

                update_query = """
                    UPDATE user
                    SET firstname = %s, lastname = %s, profile_picture = %s
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
                        "message": f"Type de changement de profile inconnu."
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

    try:
        cursor = cnx.cursor(buffered=True)

        if not user_exists(user_id, cursor):
            raise BaseException("Cet utilisateur n'existe pas.")

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
    finally:
        close_connection(cnx)


if __name__ == '__main__':
    app.run(port=8003)
