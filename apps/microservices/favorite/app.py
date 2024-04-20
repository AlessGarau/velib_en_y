from flask import Flask, request, jsonify
from mysql.connector.cursor import MySQLCursor

from database_access_layer.database import connect_to_database
from database_access_layer.models.favorite_station import FavoriteStation

app = Flask(__name__)
cnx = connect_to_database()


def favorite_station_exists(user_id: str, station_code: str, cursor: MySQLCursor) -> bool:
    """
    Checks that the favorite station targeted (user_id and station_code) exists in the db
    """

    select_query = """
        SELECT * 
        FROM favorite_station 
        WHERE user_id=%s AND station_code=%s
    """
    cursor.execute(select_query, (user_id, station_code,))
    row = cursor.fetchall()

    return len(row) > 0


@app.route('/api/favorites', methods=['GET'])
def user_favorites():
    body = request.get_json()
    user_id = body.get('user_id')

    try:
        cursor = cnx.cursor(buffered=True)

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


@app.route('/api/favorites/<station_code>', methods=['DELETE'])
def delete_favorite(station_code: str):
    body = request.get_json()
    user_id = body.get('user_id')

    try:
        cursor = cnx.cursor(buffered=True)

        if not favorite_station_exists(user_id, station_code, cursor):
            raise BaseException("Credentials are not valid. Check the user or the station's validity.")

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


@app.route('/api/favorites/<station_code>', methods=['PUT'])
def update_favorite(station_code):
    body = request.get_json()
    user_id = body.get('user_id')
    name_custom = body.get('name_custom')

    try:
        cursor = cnx.cursor(buffered=True)

        if not favorite_station_exists(user_id, station_code, cursor):
            raise BaseException(f"Favorite station {station_code} doesn't exists")

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


@app.route('/api/favorites/', methods=['POST'])
def create_favorite():
    body = request.get_json()
    station_code = body.get('station_code')
    user_id = body.get('user_id')
    name = body.get('name')
    picture = body.get('picture')
    name_custom = body.get('name_custom')

    try:
        cursor = cnx.cursor(buffered=True)

        if favorite_station_exists(user_id, station_code, cursor):
            raise BaseException(f"Favorite station {station_code} already exists")

        if not all((station_code, user_id, name, picture, name_custom,)):
            raise BaseException("Credentials are not valid.")

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


if __name__ == '__main__':
    app.run()
