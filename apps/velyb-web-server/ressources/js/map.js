// TODO - Essayer de garder dernière position en localStorage
// TODO - Si l'user est connecté, remplir la liste favorite_stations 

// Set initial view
const map = L.map('map').setView([48.8566, 2.3522], 13);
const mcg = L.markerClusterGroup();
L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    className: 'map-tiles'
}).addTo(map);

class VelybMap {
    stations_per_commune = new Object();
    favorite_stations = new Array();
    total_count = 0;

    constructor(data_url, selected_neighborhood, user_id = null) {
        this.data_url = data_url;
        this.selected_neighborhood = selected_neighborhood;
        this.user_id = user_id;
    }

    async set_stations() {
        await axios.get(this.data_url)
            .then(res => {
                this.total_count = res.data.total_count;

                const markers = res.data.results.map(station => {
                    const coordinates = [station.coordonnees_geo.lat, station.coordonnees_geo.lon];
                    const marker = L.marker(coordinates);
                    marker.bindPopup(`
                                <b>${station.name}</b>
                                <br/>
                                Nombre de vélos disponibles : ${station.numbikesavailable}
                                <br/>
                                Type : Mécanique : ${station.mechanical}/ Électrique : ${station.ebike}
                                <br/>
                                Nombre de places libres : ${station.numdocksavailable}
                            `)

                    if (!this.stations_per_commune.hasOwnProperty(station.nom_arrondissement_communes)) {
                        this.stations_per_commune[station.nom_arrondissement_communes] = new Array();
                    }
                    this.stations_per_commune[station.nom_arrondissement_communes].push({'station': station, 'marker': marker});

                    mcg.addLayer(marker);
                    return marker;
                });

                mcg.addTo(map);
                // debugger;
            })
            .catch(error => console.error(error));
    }

}

const velybMap = new VelybMap('http://localhost:8004/', 'Paris')
velybMap.set_stations();
