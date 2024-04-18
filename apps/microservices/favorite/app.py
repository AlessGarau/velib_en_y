from flask import Flask, jsonify
from database_access_layer.database import connect_to_database
from database_access_layer.models.favorite_station import FavoriteStation

app = Flask(__name__)
cnx = connect_to_database()


@app.route('/')
def index():
    # Example
    try:
        favorite_stations = []
        cursor = cnx.cursor(buffered=True)

        query = "SELECT * FROM favorite_station"
        cursor.execute(query)
        for row in cursor.fetchall():
            favorite_stations.append(FavoriteStation(*row).to_dict())
        cursor.close()

        return jsonify({'data': favorite_stations}), 200
    except BaseException as e:
        return jsonify({'message': str(e)}), 400


if __name__ == '__main__':
    app.run()
