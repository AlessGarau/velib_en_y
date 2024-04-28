import { addFavorite } from "./favorite.js";

class Stations {
    stationContainer = document.getElementsByClassName('station-container')[0]
    userId = document.cookie.split("user_id=")[1]
    constructor(dataUrl)
    {
        this.dataUrl = dataUrl
    }

    /**
     * Génération des stationCards optimisées
     * @param {Array} opendata Liste des stations
     */
    async setStationList(opendata) {
        let i = 0;
        const batchSize = 25;

        const processBatch = async () => {
            while (i < opendata.length) {
                const batch = opendata.slice(i, i + batchSize);
                await Promise.all(batch.map(async (station) => {
                    const stationCard = this.generateStationCard(station);
                    const divider = this.generateDivider()
                    this.stationContainer.appendChild(stationCard);
                    this.stationContainer.appendChild(divider);
                }));
                i += batchSize;

                // Allow the browser to update the UI and handle user input
                await new Promise(resolve => requestAnimationFrame(resolve));
            }
        };

        await processBatch();
    }

    generateStationCard(data) {
        // main station card container
        const stationCard = document.createElement('div');
        stationCard.id = data.stationcode;
        stationCard.classList.add('station-card');

        // station info container
        const stationInfos = document.createElement('div');
        stationInfos.classList.add('station-infos');

        // station name
        const stationName = document.createElement('h3');
        stationName.textContent = data.name;
        stationInfos.appendChild(stationName);

        // station commune
        const stationCommune = document.createElement('p');
        stationCommune.textContent = data.nom_arrondissement_communes;
        stationInfos.appendChild(stationCommune);

        // Append station info container
        stationCard.appendChild(stationInfos);

        if (this.userId) {
            const actions = document.createElement('div');
            actions.classList.add('actions');

            // favorite button
            const favoriteButton = document.createElement('button');
            favoriteButton.addEventListener('click', () => addFavorite(data.stationcode, data.name));


            // favorite button icon
            const favoriteIcon = document.createElement('img');
            favoriteIcon.src = 'ressources/img/fav_icon_empty.svg';
            favoriteButton.appendChild(favoriteIcon);

            // Add favorite button to actions container
            actions.appendChild(favoriteButton);

            // Add actions container to station card
            stationCard.appendChild(actions);
        }

        return stationCard;
    }

    generateDivider() {
        const divider = document.createElement('div');
        divider.classList.add('divider');

        return divider;
    }

}

export const stations = new Stations('http://localhost:8000/bridge/cache');