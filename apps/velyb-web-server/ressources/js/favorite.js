import { createNotification } from "./common.js";

const user_id = document.cookie.split("user_id=")[1];

/**
 * Ajout la station en favoris et change la future action en suppression
 * @param {string} station_code Code de la station
 * @param {string} name Nom de la station
 * @returns 
 */
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
        updateCta(station_code, 
            'add-cta', 
            'remove-cta', 
            '/ressources/img/fav_icon_full.svg', 
            () => removeFavorite(station_code, name))
    } catch (error) {
        console.error("Erreur lors de l'ajout du favori :", error);
    }
}

window.addFavorite = addFavorite

/**
 * 
 * @param {string} station_code Code de la station
 * @param {string} name Nom de la station
 * @returns 
 */
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
        updateCta(station_code, 
            'remove-cta', 
            'add-cta',
            '/ressources/img/fav_icon_empty.svg', 
            () => addFavorite(station_code, name))
    } catch (error) {
        console.error("Erreur lors de la suppression du favori :", error);
    }
}

window.removeFavorite = removeFavorite

function updateCta(station_code, oldSelector, newSelector,iconSrc, callBackListener) {
    const actions = document.getElementById(station_code).querySelector('.actions');
    const oldButton = Array.from(actions.childNodes).find(action => action.className === oldSelector);

    const newButton = document.createElement('button');
    newButton.classList.add(newSelector)
    const favoriteIcon = document.createElement('img');
    favoriteIcon.src = iconSrc;
    newButton.appendChild(favoriteIcon)
    newButton.addEventListener('click', () => callBackListener());
    
    actions.replaceChild(newButton, oldButton);
}