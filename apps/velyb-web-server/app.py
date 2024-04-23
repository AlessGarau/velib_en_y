from flask import Flask, jsonify
from socket_communication.client_socket import ClientSocket

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.get("/api/stations")
def stations():
    try:
        # to fix : 8004 in .env
        socket = ClientSocket(8004)
        response = socket.read()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error : {e}"
        }), 500

if __name__ == '__main__':
    app.run()

