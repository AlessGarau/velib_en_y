from flask import jsonify
import requests


def get_stations():
    res = requests.get('http://api-caching-server:8004/')

    return jsonify(res.json()), res.status_code
