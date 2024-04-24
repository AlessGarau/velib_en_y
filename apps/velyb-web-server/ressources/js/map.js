// TODO - Essayer de garder dernière position en localStorage
// TODO - Si l'user est connecté, remplir la liste favorite_stations 

// Set initial view to Paris
const map = L.map('map').setView([48.8566, 2.3522], 13);
L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    className: 'map-tiles'
}).addTo(map);

class VelybMap {
    stations = [];
    favorite_stations = [];
    neighborhoods = new Set();
    total_count = 0;

    constructor(data_url, selected_neighborhood, user_id = null) {
        this.data_url = data_url;
        this.selected_neighborhood = selected_neighborhood;
        this.user_id = user_id;
    }

    set_stations() {
        axios.get(this.data_url)
            .then(res => {
                this.total_count = res.data.total_count;
                res.data.results.forEach(station => {
                    this.neighborhoods.add(station.nom_arrondissement_communes);
                    if (station.nom_arrondissement_communes === this.selected_neighborhood) {
                        const coordinates = [station.coordonnees_geo.lat, station.coordonnees_geo.lon];
                        const marker = L.marker(coordinates).addTo(map);
                        marker.bindPopup(`
                            <b>${station.name}</b>
                            <br/>
                            Nombre de vélos disponibles : ${station.numbikesavailable}
                            <br/>
                            Type : Mécanique : ${station.mechanical}/ Électrique : ${station.ebike}
                            <br/>
                            Nombre de places libres : ${station.numdocksavailable}
                        `)
                    }
                })
                // debugger;
            })
            .catch(error => console.error(error));
    }

}

const velybMap = new VelybMap('http://localhost:8004/', 'Paris')
velybMap.set_stations()
