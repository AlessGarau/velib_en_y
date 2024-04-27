import { createNotification } from "./common.js";

const user_id = document.cookie.split("user_id=")[1];

async function addFavorite(station_code, name) {
    try {
        const favoriteCredentials = {
            user_id: user_id,
            station_code: station_code,
            name: name,
            picture: "x", // N'est même pas sur la maquette donc pas utilisé mais ok
            name_custom: name
        };

        const res = await fetch('http://localhost:8002/api/favorites/', {
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
    } catch (error) {
        console.error("Erreur lors de l'ajout du favori :", error);
    }
}

window.addFavorite = addFavorite

async function removeFavorite(station_code, name) {
    try {
        const favoriteCredentials = {
            user_id: user_id
        };
        
        const res = await fetch(`http://localhost:8002/api/favorites/${station_code}`, {
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
    } catch (error) {
        console.error("Erreur lors de la suppression du favori :", error);
    }
}

window.removeFavorite = removeFavorite
