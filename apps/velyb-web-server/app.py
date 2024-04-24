import json
from flask import Flask, make_response, redirect, render_template, request, session
import requests
import requests.cookies
from loaders import user_loaders

app = Flask(__name__,
            static_folder='ressources/',)
app.secret_key = b"4072bd90fe380021dd09cb1dc213a782b315656cf0e920866118ea0c2a3bf933"

base_metadata = {
    'css_paths': ['ressources/css/style.css', 'ressources/css/header.css', 'ressources/css/tab.css', "ressources/css/map.css"],
    'js_paths': ['/ressources/js/common.js', '/ressources/js/map.js'],
    'nav_items': {
        'unauthorized': [
            {'name': 'Accueil', 'link': '/', 'key': 'home'},
            {'name': 'Connexion', 'link': 'login', 'key': 'auth'},
        ],
        'authorized': [
            {'name': 'Accueil', 'link': '/', 'key': 'home'},
            {'name': 'Réglages', 'link': 'settings?type=profile', 'key': 'settings'},
            {'name': 'Déconnexion', 'link': 'logout', 'key': 'logout'}
        ]
    }
}


@app.route('/')
def index():
    user = user_loaders.get_user_from_cookie()
    metadata = {
        **base_metadata,

    }

    if user:
        metadata["user"] = user
    metadata["title"] = "Accueil"
    metadata["key"] = "home"
    metadata["station_type"] = "all"

    return render_template('/layouts/index.html', **metadata)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        user = user_loaders.get_user_from_cookie()

        if user:
            return redirect('/')

        metadata = {
            **base_metadata,
            "css_paths": [*base_metadata["css_paths"], "ressources/css/auth.css"]
        }
        metadata["title"] = "Connexion"
        metadata["auth_type"] = "login"
        metadata["key"] = "auth"
        metadata["message"] = request.args.get("m")
        metadata["status"] = request.args.get("status")

        return render_template('/layouts/auth.html', **metadata)
    elif request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        if not all((email, password)):
            return redirect('/login?m=Email and password are required&status=error')

        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://microservices_authentification:8001/api/authentification/login',
                                 json={
                                     "email": email,
                                     "password": password
                                 },
                                 headers=headers)
        data = response.json()

        if response.ok:
            user = data.get("data")["user"]

            res = make_response(redirect("/"))
            res.set_cookie('user', json.dumps(user))

            return res
        else:
            message = data.get("message")
            return redirect(f"/login?m={message}&status=error")


@app.route('/register')
def register():
    user = user_loaders.get_user_from_cookie()

    if user:
        return redirect('/')

    metadata = {
        **base_metadata,
        "css_paths": [*base_metadata["css_paths"], "ressources/css/auth.css"]
    }
    metadata["title"] = "Inscription"
    metadata["auth_type"] = "register"
    metadata["key"] = "auth"

    return render_template('/layouts/auth.html', **metadata)


@app.route('/settings')
def settings():
    user = user_loaders.get_user_from_cookie()
    setting_type_param = request.args.get("type")

    if not user or not setting_type_param:
        return redirect('/')

    metadata = {
        **base_metadata,
    }
    metadata["user"] = user
    metadata["title"] = "Réglages"
    metadata["key"] = "settings"
    metadata["setting_type"] = setting_type_param

    return render_template('/layouts/settings.html', **metadata)


@app.route('/favorites')
def favorites():
    user = user_loaders.get_user_from_cookie()

    if not user:
        return redirect('/')

    metadata = {
        **base_metadata,
    }
    metadata["user"] = user
    metadata["title"] = "Favoris"
    metadata["key"] = "favorites"
    metadata["station_type"] = "favorites"

    return render_template('/layouts/favorites.html', **metadata)


@app.route('/logout')
def logout():
    response = requests.get('http://microservices_authentification:8001/api/authentification/logout',
                            cookies=request.cookies)

    if response.ok:
        res = make_response(redirect("/", code=302))
        res.delete_cookie('user')

        return res
    else:
        message = response.json().get('message')
        res = make_response(redirect(f"/?message={message}&status=error", code=302))

        return res


@app.route('/error/<code>')
def error(code=404):
    return render_template(f"/layouts/{code}.html")


if __name__ == '__main__':
    app.run()
