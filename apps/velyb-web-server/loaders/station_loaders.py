import os
from flask import jsonify
import requests

cache_host = os.getenv('CACHE_HOST')


def get_stations():
    res = requests.get(f'http://{cache_host}:8004/')

    return jsonify(res.json()), res.status_code
