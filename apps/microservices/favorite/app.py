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

    query = "SELECT * FROM favorite_station WHERE user_id=%s AND station_code=%s"
    cursor.execute(query, (user_id, station_code,))
    row = cursor.fetchall()

    return len(row) > 0


@app.route('/api/favorites', methods=['GET'])
def user_favorites():
    body = request.get_json()
    user_id = body.get('user_id')

    try:
        cursor = cnx.cursor(buffered=True)

        query = "SELECT * FROM favorite_station WHERE user_id=%s"
        cursor.execute(query, (user_id,))

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

        query = "DELETE FROM favorite_station WHERE station_code = %s AND user_id = %s"
        cursor.execute(query, (station_code, user_id,))
        cursor.close()

        return jsonify({
            'success': True
        }), 200
    except BaseException as e:
        return jsonify({
            'message': str(e),
            'success': False
        }), 400

    # First check if station code exists in favorites with SELECT * FROM favorite_station WHERE station_code = station_code AND user_id = user_id
    # If doesn't exist, return Error 404

    # try except
    # Execute query to DELETE FROM favorite_station WHERE station_code = station_code
    # return 200


@app.route('/api/favorites/<station_code>', methods=['PUT'])
def update_favorite(station_code):
    # Authorization with Auth Microservice
    # If not authorized, return Error 401
    # Else retrieve user_id

    # First check if station code exists in favorites with SELECT * FROM favorite_station WHERE station_code = station_code AND user_id = user_id
    # If doesn't exist, return Error 404

    data = request.get_json()
    # Validate inputs
    # picture, name_custom

    # try except
    # Execute query to UPDATE favorite_station SET ...values
    # return 200
    return jsonify({'foo': 'bar'}), 200


@app.route('/api/favorites/', methods=['POST'])
def create_favorite():
    # Authorization with Auth Microservice
    # If not authorized, return Error 401
    # Else retrieve user_id

    # First check if station code already exists in favorites with SELECT * FROM favorite_station WHERE station_code = station_code AND user_id = user_id
    # If it does exist, return Error 400

    data = request.get_json()
    # Validate inputs
    # picture, name_custom, name, station_code

    # try except
    # Execute query to INSERT INTO favorite_station ...values
    # return 200
    return jsonify({'foo': 'bar'}), 200


if __name__ == '__main__':
    app.run()
