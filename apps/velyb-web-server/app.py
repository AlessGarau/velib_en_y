from flask import Flask, redirect, render_template, request
import requests
from loaders import user_loaders

app = Flask(__name__,
            static_folder='ressources/',)

base_metadata = {
    'css_paths': ['ressources/css/style.css', 'ressources/css/header.css', 'ressources/css/tab.css'],
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

    return render_template('/layouts/index.html', **metadata)


@app.route('/login')
def login():
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

    return render_template('/layouts/auth.html', **metadata)


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
    metadata["title"] = "Favoris"
    metadata["key"] = "favorites"

    return render_template('/layouts/favorites.html', **metadata)


if __name__ == '__main__':
    app.run()
