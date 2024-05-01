import { addFavorite, removeFavorite } from "./favorite.js";

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
    async setStationList(opendata, favoriteStations, areInFavorite) {
        let i = 0;
        const batchSize = 25;

        const processBatch = async () => {
            while (i < opendata.length) {
                const batch = opendata.slice(i, i + batchSize);
                await Promise.all(batch.map(async (station) => {
                    const stationCard = this.generateStationCard(station, favoriteStations.find(favoriteStation => favoriteStation.station_code === station.stationcode), areInFavorite);
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

    generateStationCard(data, isFavoriteStation, areInFavorite) {
        // main station card container
        const stationCard = document.createElement('div');
        stationCard.id = data.stationcode;
        stationCard.classList.add('station-card');

        // station info container
        const stationInfos = document.createElement('div');
        stationInfos.classList.add('station-infos');

        // station name
        const stationName = document.createElement('h3');
        stationName.textContent = areInFavorite ? data.name_custom : data.name;
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

            // favorite button icon
            const favoriteIcon = document.createElement('img');

            // debugger
            if(isFavoriteStation){
                // favorite button
                favoriteButton.addEventListener('click', () => removeFavorite(data.stationcode, data.name));
                favoriteButton.classList.add('remove-cta');
                // favorite button icon
                favoriteIcon.src = 'ressources/img/fav_icon_full.svg';
            } else {
                // favorite button
                favoriteButton.addEventListener('click', () => addFavorite(data.stationcode, data.name));
                favoriteButton.classList.add('add-cta');
                // favorite button icon
                favoriteIcon.src = 'ressources/img/fav_icon_empty.svg';
            }

            // favorite button icon
            favoriteButton.appendChild(favoriteIcon);

            // Add favorite button to actions container
            actions.appendChild(favoriteButton);

            if(areInFavorite){
                // edit button
                const editButton = document.createElement('button');
                editButton.addEventListener('click', () => {this.toggleEditForm(data.station_code)});
                editButton.classList.add('edit-cta');
                const editIcon = document.createElement('img');
                editIcon.src = 'ressources/img/edit_icon.svg';
                editButton.appendChild(editIcon);
                actions.appendChild(editButton);
            }

            // Add actions container to station card
            stationCard.appendChild(actions);

            if(areInFavorite){
                // form
                const editForm = document.createElement('form');
                editForm.method='POST';
                editForm.id = 'form-' + data.station_code;
                editForm.classList.add('none');

                // div Element
                const divElement = document.createElement('div');

                // label
                const labelName = document.createElement('label');
                labelName.textContent = "Nom du favori";
                labelName.setAttribute('for', 'name_custom');

                // input
                const inputName = document.createElement('input');
                inputName.type = 'text';
                inputName.id = 'name_custom';
                inputName.name = 'name_custom';
                inputName.placeholder = data.name;
                inputName.value = data.name_custom;

                divElement.appendChild(labelName);
                divElement.appendChild(inputName);

                // hide input
                const inputStationCode = document.createElement('input');
                inputStationCode.type = 'hidden';
                inputStationCode.id = 'station_code';
                inputStationCode.name = 'station_code';
                inputStationCode.value = data.station_code;

                // button
                const submitButton = document.createElement('button');
                submitButton.type = 'submit';
                submitButton.textContent = 'Enregistrer le changement';

                editForm.appendChild(divElement);
                editForm.appendChild(inputStationCode);
                editForm.appendChild(submitButton);
                stationCard.appendChild(editForm);
            }
        }

        return stationCard;
    }

    generateDivider() {
        const divider = document.createElement('div');
        divider.classList.add('divider');

        return divider;
    }

    toggleEditForm(stationCode){
        const editForm = document.getElementById('form-' + stationCode);
        if(editForm.classList.contains('none')){
            editForm.classList.remove('none');
        } else {
            editForm.classList.add('none');
        }
    }

}

export const stations = new Stations('http://localhost:8000/bridge/cache');