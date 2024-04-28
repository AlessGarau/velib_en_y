import json
from flask import Response, jsonify
import requests

microservice_endpoint = "http://microservices_favorite:8002/api/favorites/"


def get_favorites(user_id) -> Response:
    res = requests.get(f"{microservice_endpoint}{user_id}")
    return jsonify(res.json()), res.status_code


def create_favorite(body) -> Response:
    res = requests.post(microservice_endpoint,
                        json=body)

    return jsonify(res.json()), res.status_code


def remove_favorite(body, station_code) -> Response:
    res = requests.delete(f"{microservice_endpoint}{station_code}",
                          json=body)
    return jsonify(res.json()), res.status_code
