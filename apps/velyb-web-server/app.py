from flask import Flask, render_template, request
import requests
from loaders import user_loaders

app = Flask(__name__,
            static_folder='ressources/',)

base_metadata = {
    'css_paths': ['ressources/css/style.css', 'ressources/css/sidebar.css'],
    'nav_items': {
        'unauthorized': [
            {'name': 'Accueil', 'link': '/'},
            {'name': 'Connexion', 'link': 'login'},
        ],
        'authorized': [
            {'name': 'Accueil', 'link': '/'},
            {'name': 'Réglages', 'link': 'settings'},
            {'name': 'Déconnexion', 'link': 'logout'}
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

    return render_template('/layouts/index.html', **metadata)


@app.route('/login')
def login():
    metadata = {
        **base_metadata,
    }
    metadata["title"] = "Connexion"
    metadata["auth_type"] = "login"

    return render_template('/layouts/auth.html', **metadata)


@app.route('/register')
def register():
    metadata = {
        **base_metadata,
    }
    metadata["title"] = "Inscription"
    metadata["auth_type"] = "register"

    return render_template('/layouts/auth.html', **metadata)


@app.route('/settings')
def settings():
    metadata = {
        **base_metadata,
    }
    metadata["title"] = "Réglages"

    return render_template('/layouts/settings.html', **metadata)


@app.route('/favorites')
def favorites():
    metadata = {
        **base_metadata,
    }
    metadata["title"] = "Favoris"

    return render_template('/layouts/favorites.html', **metadata)


if __name__ == '__main__':
    app.run()
