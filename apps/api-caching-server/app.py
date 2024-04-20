from flask import Flask, jsonify
import socket
import requests
import time
app = Flask(__name__)

api_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=100"
last_api_call = 0


def check_api_call():
    global last_api_call
    current_time = time.time()
    if current_time - last_api_call > 300:
        last_api_call = current_time
        return True
    else:
        return False


def call_api():
    api_data = requests.get(api_url).json()
    velib_count = api_data.get("total_count")
    if check_api_call():
        for offset in range(0, velib_count, 100):
            response = requests.get(api_url + f"&offset={offset}")
            new_data = response.json()
            api_data["results"].append(new_data)
        return api_data
    return api_data


first_api_call = call_api()


@ app.route('/')
def index():
    return '<h1>Streamez <a href="https://open.spotify.com/track/6TzeXZyF3ULjwFz64eoXUc?si=a944a36fff674166">BU$HI </a></h1>'


@ app.route('/get_all_velib', methods=['GET'])
def get_data():
    all_velib = call_api()
    return jsonify(all_velib)
