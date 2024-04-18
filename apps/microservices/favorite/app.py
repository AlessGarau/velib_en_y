from flask import Flask, jsonify
from database_access_layer.database import connect_to_database
from database_access_layer.models.favorite_station import FavoriteStation

app = Flask(__name__)
cnx = connect_to_database()


@app.route('/')
def index():
    # Authorization, should retrieve user_id or return 401
    user_id = 1

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

        return jsonify({'data': favorite_stations}), 200
    except BaseException as e:
        return jsonify({'message': str(e)}), 400


if __name__ == '__main__':
    app.run()
