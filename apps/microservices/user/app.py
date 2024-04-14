from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>ODAMA RASENGAN !!!!!!</h1>"


if __name__ == '__main__':
    app.run()