import json

from flask import Flask, request, jsonify
from mysql.connector.cursor import MySQLCursor

from database_access_layer.database import connect_to_database, close_connection
from database_access_layer.models.favorite_station import FavoriteStation

app = Flask(__name__)


def favorite_station_exists(user_id: str, station_code: str, cursor: MySQLCursor, check_user: bool = False) -> bool:
    """
    Checks that the favorite station targeted (user_id and station_code) exists in the db
    """

    if check_user:
        select_query = """
            SELECT * 
            FROM user
            WHERE user_id=%s
        """
        cursor.execute(select_query, (user_id,))
        user = cursor.fetchone()

        if not (user and len(user) > 0):
            raise BaseException("Erreur lors de la recherche de l'utilisateur, impossibilité d'acceder à ses favoris.")

    select_query = """
        SELECT * 
        FROM favorite_station 
        WHERE user_id=%s AND station_code=%s
    """
    cursor.execute(select_query, (user_id, station_code,))
    favorite_stations = cursor.fetchall()

    return len(favorite_stations) > 0


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


@app.route('/api/favorites/<user_id>', methods=['GET'])
def user_favorites(user_id):
    cnx = connect_to_database()

    try:
        cursor = cnx.cursor(buffered=True)

        if not user_exists(user_id, cursor):
            raise BaseException("Cet utilisateur n'existe pas.")

        select_query = """
            SELECT *
            FROM favorite_station
            WHERE user_id=%s
        """
        cursor.execute(select_query, (user_id,))

        favorite_stations = []
        rows = cursor.fetchall()
        for row in rows:
            favorite_station = FavoriteStation(*row)
            favorite_stations.append(favorite_station.to_dict())

        cursor.close()

        return jsonify({
            'data': favorite_stations,
            'success': True
        }), 200
    except BaseException as e:
        return jsonify({
            'message': str(e),
            'success': False
        }), 400
    finally:
        close_connection(cnx)


@app.route('/api/favorites/<station_code>', methods=['DELETE'])
def delete_favorite(station_code: str):
    cnx = connect_to_database()

    body = request.get_json()
    user_id = body.get('user_id')

    try:
        cursor = cnx.cursor(buffered=True)

        if not (user_exists(user_id, cursor)):
            raise BaseException("Cet utilisateur n'existe pas.")

        if not favorite_station_exists(user_id, station_code, cursor):
            raise BaseException(f"La station {station_code} ne se trouve pas dans vos favoris.")

        delete_query = """
            DELETE FROM favorite_station 
            WHERE station_code = %s AND user_id = %s
        """
        cursor.execute(delete_query, (station_code, user_id,))
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


@app.route('/api/favorites/<station_code>', methods=['PUT'])
def update_favorite(station_code):
    cnx = connect_to_database()

    body = request.get_json()
    user_id = body.get('user_id')
    name_custom = body.get('name_custom')

    try:
        cursor = cnx.cursor(buffered=True)

        if not all((user_id, name_custom,)):
            raise BaseException("Veuillez remplir l'intégralité des champs.")

        if not user_exists(user_id, cursor):
            raise BaseException("Cet utilisateur n'existe pas.")

        if not favorite_station_exists(user_id, station_code, cursor, True):
            raise BaseException(f"La station {station_code} ne se trouve pas dans vos favoris.")

        update_query = """
            UPDATE favorite_station
            SET name_custom = %s
            WHERE user_id = %s AND station_code = %s
        """
        cursor.execute(update_query, (name_custom, user_id, station_code,))
        cnx.commit()

        select_query = """
            SELECT * 
            FROM favorite_station 
            WHERE user_id = %s AND station_code = %s
        """
        cursor.execute(select_query, (user_id, station_code,))
        updated_station = FavoriteStation(*cursor.fetchone())

        cursor.close()

        return jsonify({
            'data': updated_station.to_dict(),
            'success': True
        }), 200
    except BaseException as e:
        return jsonify({
            'message': str(e),
            'success': False
        }), 400
    finally:
        close_connection(cnx)


@app.route('/api/favorites/', methods=['POST'])
def create_favorite():
    cnx = connect_to_database()

    body = request.get_json()
    user_id = body.get('user_id')
    station_code = body.get('station_code')
    name = body.get('name')
    picture = body.get('picture')
    name_custom = body.get('name_custom')

    try:
        cursor = cnx.cursor(buffered=True)

        if not (user_exists(user_id, cursor)):
            raise BaseException("Cet utilisateur n'existe pas.")

        if not all((station_code, user_id, name, picture, name_custom,)):
            raise BaseException("Veuillez remplir l'intégralité des champs.")

        if favorite_station_exists(user_id, station_code, cursor, True):
            raise BaseException(f"La station {station_code} se trouve déja dans vos favoris.")

        insert_query = """INSERT INTO favorite_station VALUES(%s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, (station_code, user_id, name, picture, name_custom,))
        cnx.commit()

        select_query = """
            SELECT * 
            FROM favorite_station 
            WHERE user_id = %s AND station_code = %s
        """
        cursor.execute(select_query, (user_id, station_code,))
        favorite_station = FavoriteStation(*cursor.fetchone())

        cursor.close()

        return jsonify({
            'data': favorite_station.to_dict(),
            'success': True
        }), 201
    except BaseException as e:
        return jsonify({
            'message': str(e),
            'success': False
        }), 400
    finally:
        close_connection(cnx)


def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = 'http://localhost:8000'
    return response


app.after_request(after_request)

if __name__ == '__main__':
    app.run(port=8002)
