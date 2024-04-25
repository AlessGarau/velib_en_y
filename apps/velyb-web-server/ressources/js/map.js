// TODO - Essayer de garder dernière position en localStorage

const user_id = document.cookie.split("user_id=")[1];
const is_favorite_page = window.location.pathname.includes("favorites");

// Set initial view
const map = L.map("map").setView([48.8566, 2.3522], 13);
const mcg = L.markerClusterGroup();
L.tileLayer("https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  className: "map-tiles",
}).addTo(map);

class VelybMap {
  stations_per_commune = new Object();
  favorite_stations = new Array();
  total_count = 0;

  constructor(data_url, user_id = null, is_favorite_map) {
    this.data_url = data_url;
    this.user_id = user_id;
  }

  async set_stations() {
    const res = await axios.get(this.data_url);
    this.total_count = res.data.total_count;

    const markers = res.data.results.map((station) => {
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
                        `);

      if (!this.stations_per_commune.hasOwnProperty(station.nom_arrondissement_communes)) {
        this.stations_per_commune[station.nom_arrondissement_communes] = new Array();
      }
      this.stations_per_commune[station.nom_arrondissement_communes].push({ station: station, marker: marker });

      mcg.addLayer(marker);
      return marker;
    });

    mcg.addTo(map);
    // debugger;
  }
}

const velybMap = new VelybMap("http://localhost:8004/", user_id ? user_id : null, is_favorite_page);
velybMap.set_stations();
