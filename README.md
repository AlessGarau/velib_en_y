# Velyb

## Introduction

Le projet Velyb est une application web développée en Python à l'aide du framework Flask et du moteur de template Jinja. Son objectif est de fournir une interface conviviale pour visualiser les stations Vélib disponibles dans la ville de Paris.

## Fonctionnalités

- Consultation des stations Vélib sur une carte interactive.
- Visualisation des détails de chaque station (nombre de vélos disponibles, types de vélos disponibles, et nombre de places libres).
- Ajout de stations à une liste de favoris.
- Création d'un compte utilisateur.
- Modification des informations personnelles ainsi que du mot de passe de l'utilisateur.

## Installation

1. Cloner le dépôt Github :

```bash
git clone https://github.com/AlessGarau/velyb
```

2. Accéder au répertoire du projet :

```bash
cd velyb
```

3. Lancer le projet :

```bash
# Sans Docker
source ./setup.sh all
```

```bash
# Avec Docker
docker compose up
```

4. Accédez à l'application dans votre navigateur :

```
http://localhost:8000
```

## Fonctionnement Technique

### Architecture

L'application est basée sur une architecture de microservices (user, authentification, favorite), avec un serveur web Flask et un serveur FTP pour les requêtes API.

### Technologies Utilisées

- Python3 
- Flask
- Jinja
- Leaflet & OpenStreetMap
- Api de la ville de Paris

## Auteurs

- [@LTOssian](https://github.com/LTOssian)
- [@heitzjulien](https://github.com/heitzjulien)
- [@Kobrae-San](https://github.com/Kobrae-San)
- [@AlessGarau](https://github.com/AlessGarau)
- [@Nyoote](https://github.com/Nyoote)
- [@LeBenjos](https://github.com/LeBenjos)
