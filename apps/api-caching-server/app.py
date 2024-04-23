import socket
import requests
import time


api_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=100"
last_api_call = 0

data_cached = requests.get(api_url).json()
velib_count = data_cached.get("total_count")


def check_api_call():
    global last_api_call
    current_time = time.time()
    if current_time - last_api_call > 300:
        last_api_call = current_time
        return True
    else:
        return False


def call_api():
    global data_cached
    global velib_count
    if check_api_call():
        data = requests.get(api_url).json()
        velib_count = data.get("total_count")
        for offset in range(0, velib_count, 100):
            response = requests.get(api_url + f"&offset={offset}")
            new_data = response.json()
            data["results"].append(new_data)
        data_cached = data
    return data_cached


HOST = 'localhost'
PORT = 8004


def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection received from {address}")

        data = call_api()
        client_socket.sendall(str(data).encode())

        client_socket.close()


tcp_server()
