import { createNotification } from "./common.js";

const user_id = document.cookie.split("user_id=")[1];

export async function addFavorite(station_code, name) {
    try {
        const favoriteCredentials = {
            user_id: user_id,
            station_code: station_code,
            name: name,
            picture: "NULL", // N'est même pas sur la maquette donc pas utilisé mais ok
            name_custom: name
        };

        const res = await fetch('http://localhost:8000/bridge/favorites/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(favoriteCredentials)
        });

        const resData = await res.json();
        if (!res.ok) {
            console.error("Erreur lors de l'ajout du favori:", resData.message);
            createNotification(resData.message, 'error')
            return;
        }

        createNotification(`Station ${name} ajoutée aux favoris`, 'success')
        const stationCard = document.getElementById(station_code);
        const button = stationCard.getElementsByTagName('button')[0];
        const image = stationCard.getElementsByTagName('img')[0];
        button.removeEventListener('click', addFavorite);
        button.addEventListener('click', () => {
            removeFavorite(station_code, name)
        });
        image.src = '/ressources/img/fav_icon_full.svg';
    } catch (error) {
        console.error("Erreur lors de l'ajout du favori :", error);
    }
}

window.addFavorite = addFavorite

export async function removeFavorite(station_code, name) {
    try {
        const favoriteCredentials = {
            user_id: user_id
        };

        const res = await fetch(`http://localhost:8000/bridge/favorites/${station_code}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(favoriteCredentials)
        });

        const resData = await res.json();
        if (!res.ok) {
            console.error("Erreur lors de la suppression du favori:", resData.message);
            createNotification(resData.message, 'error');
            return;
        }

        createNotification(`Station ${name} supprimée des favoris`, 'success');
        const stationCard = document.getElementById(station_code);
        const button = stationCard.getElementsByTagName('button')[0];
        const image = stationCard.getElementsByTagName('img')[0];
        button.removeEventListener('click', removeFavorite);
        button.addEventListener('click', () => {
            addFavorite(station_code, name)
        });
        image.src = '/ressources/img/fav_icon_empty.svg';
    } catch (error) {
        console.error("Erreur lors de la suppression du favori :", error);
    }
}

window.removeFavorite = removeFavorite
