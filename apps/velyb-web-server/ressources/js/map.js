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

const favoritesResJson = `{
  "data": [
      {
          "name": "Gabriel Lamé",
          "name_custom": "Tah bogota lol hihi",
          "picture": "wouh",
          "station_code": "12031",
          "user_id": 1
      },
      {
          "name": "Bois de Vincennes.",
          "name_custom": "bois",
          "picture": "photo",
          "station_code": "12041",
          "user_id": 1
      },
      {
          "name": "11 Novembre 1918 - 8 Mai 1945",
          "name_custom": "date",
          "picture": "wouh",
          "station_code": "45003",
          "user_id": 1
      },
      {
          "name": " Saint-Séverin - Saint-Michel",
          "name_custom": "saint",
          "picture": "idk",
          "station_code": "5033",
          "user_id": 1
      }
  ],
  "success": true
}`;
let stationIconSvg = '<svg width="20" height="24" viewBox="0 0 20 24" fill="none" xmlns="http://www.w3.org/2000/svg">' +
'<path d="M19 10C19 17 10 23 10 23C10 23 1 17 1 10C1 7.61305 1.94821 5.32387 3.63604 3.63604C5.32387 1.94821 7.61305 1 10 1C12.3869 1 14.6761 1.94821 16.364 3.63604C18.0518 5.32387 19 7.61305 19 10Z" fill="#3574D3" fill-opacity="0.3"/>'+
'<path d="M10 13C11.6569 13 13 11.6569 13 10C13 8.34315 11.6569 7 10 7C8.34315 7 7 8.34315 7 10C7 11.6569 8.34315 13 10 13Z" fill="#3574D3" fill-opacity="0.3"/>'+
'<path d="M19 10C19 17 10 23 10 23C10 23 1 17 1 10C1 7.61305 1.94821 5.32387 3.63604 3.63604C5.32387 1.94821 7.61305 1 10 1C12.3869 1 14.6761 1.94821 16.364 3.63604C18.0518 5.32387 19 7.61305 19 10Z" stroke="#7F56D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'+
'<path d="M10 13C11.6569 13 13 11.6569 13 10C13 8.34315 11.6569 7 10 7C8.34315 7 7 8.34315 7 10C7 11.6569 8.34315 13 10 13Z" stroke="#7F56D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'+
'</svg>'

let stationIconSvgUrl = 'data:image/svg+xml;base64,' + btoa(stationIconSvg);

let stationIcon = L.icon({
iconUrl: stationIconSvgUrl,
iconSize: [32, 50], 
iconAnchor: [16, 32],
popupAnchor: [0, -32]
});

let favoriteStationIconSvg = '<svg width="22" height="22" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">'+
'<path d="M11 1L14.09 7.26L21 8.27L16 13.14L17.18 20.02L11 16.77L4.82 20.02L6 13.14L1 8.27L7.91 7.26L11 1Z" fill="#3574D3" fill-opacity="0.3" stroke="#7F56D9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'+
'</svg>'

let favoriteStationIconSvgUrl = 'data:image/svg+xml;base64,' + btoa(favoriteStationIconSvg);

let favoriteStationIcon = L.icon({
iconUrl: favoriteStationIconSvgUrl,
iconSize: [32, 50], 
iconAnchor: [16, 32],
popupAnchor: [0, -32]
});


class VelybMap {
  stations_per_commune = new Object();
  favorite_stations = new Array();
  total_count = 0;

  constructor(data_url, user_id = null, is_favorite_map) {
    this.data_url = data_url;
    this.user_id = user_id;
    this.is_favorite_map = is_favorite_map
  }

  async set_stations() {
    try {
      const response = await fetch(this.data_url);
      if (!response.ok) {
        throw new Error('Network response not ok');
      }
      const data = await response.json();
      this.total_count = data.total_count;

      let favoriteDataStation = data.results
      if (this.is_favorite_map){
        const favoritesData = JSON.parse(favoritesResJson);
        favoritesData.data.forEach(station => {
        this.favorite_stations.push(station.station_code);
      });
      }
      favoriteDataStation = favoriteDataStation.filter(station => this.favorite_stations.includes(station.stationcode))
      const allDataStation = data.results;
      const dataStation = is_favorite_page ? favoriteDataStation : allDataStation;

      const markers = dataStation.map((station) => {
        const coordinates = [station.coordonnees_geo.lat, station.coordonnees_geo.lon];
        const icon = is_favorite_page ? favoriteStationIcon : stationIcon;
        const marker = L.marker(coordinates, {icon : icon});
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
          this.stations_per_commune[station.nom_arrondissement_communes] = [];
        }
        this.stations_per_commune[station.nom_arrondissement_communes].push({ station: station, marker: marker });

        mcg.addLayer(marker);
        return marker;
      });
      mcg.addTo(map);
    } catch (error) {
      console.error('Error setting stations:', error);
    }
  }
}

const velybMap = new VelybMap("http://localhost:8004/", user_id ? user_id : null, is_favorite_page);
velybMap.set_stations();

