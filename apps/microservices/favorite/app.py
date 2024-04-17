from flask import Flask, request, jsonify
from database.database import connect_to_database

app = Flask(__name__)


@app.route('/api/favorites', methods=['GET'])
def user_favorites():
    # Authorization with Auth Microservice
    # If not authorized, return Error 401
    # Else retrieve user_id
    user_id = 1

    try:
        # DB Connection
        conn = connect_to_database()

        # Execute query to SELECT * FROM favorite_station WHERE user_id = user_id
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM favorite_station WHERE user_id = %s", (user_id,))
        user_favorites = cursor.fetchall()

        # Return json with favorites items
        return jsonify({'data': user_favorites}), 200

    except BaseException as e:
        return jsonify({'message': str(e)}), 400


@app.route('/api/favorites/<station_code>', methods=['DELETE'])
def delete_favorite(station_code):
    # Authorization with Auth Microservice
    # If not authorized, return Error 401
    # Else retrieve user_id

    # First check if station code exists in favorites with SELECT * FROM favorite_station WHERE station_code = station_code AND user_id = user_id
    # If doesn't exist, return Error 404

    # try except
    # Execute query to DELETE FROM favorite_station WHERE station_code = station_code
    # return 200
    return jsonify({'foo': 'bar'}), 200


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
