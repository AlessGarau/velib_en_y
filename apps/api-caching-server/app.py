from flask import Flask, jsonify
import socket
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Streamez <a href="https://open.spotify.com/track/6TzeXZyF3ULjwFz64eoXUc?si=a944a36fff674166">BU$HI </a></h1>'


@app.route('/get_all_velib', methods=['GET'])
def get_data():
    response = requests.get(
        'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=100')
    data = response.json()

    return jsonify(data)


@app.route('/guest', methods=['GET'])
def get_data_guest():
    response = requests.get(
        'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=100')
    data = response.json()
    return data


@app.route('/get_favorite',  methods=['GET'])
def get_favorite():
    response = requests.get(
        'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?where=stationcode%3D%2219029%22&limit=100')
    data = response.json()
    return data
