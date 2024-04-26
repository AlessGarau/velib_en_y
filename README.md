# Velyb

## Introduction

Le projet Velyb est une application web développée en Python à l'aide du framework Flask et du moteur de template Jinja. Son objectif est de fournir une interface conviviale pour visualiser les stations Vélib disponibles en utilisant l'API de la ville de Paris.

## Fonctionnalités

- Affichage des stations Vélib sur une carte interactive.
- Ajouter des stations en favoris.

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

L'application est construite autours de microservices, d'un serveur web flask et d'un serveur ftp pour les requetes api.

### Technologies Utilisées

- Python 3.x
- Flask
- Jinja
- Map
- Api de la ville de Paris

## Auteurs

- [@LTOssian](https://github.com/LTOssian)
- [@heitzjulien](https://github.com/heitzjulien)
- [@Kobrae-San](https://github.com/Kobrae-San)
- [@AlessGarau](https://github.com/AlessGarau)
- [@Nyoote](https://github.com/Nyoote)
- [@LeBenjos](https://github.com/LeBenjos)
