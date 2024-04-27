// TODO - Essayer de garder dernière position en localStorage

const userId = document.cookie.split("user_id=")[1];
const isFavoritePage = window.location.pathname.includes("favorites");

// Set initial view
const map = L.map("map").setView([48.8566, 2.3522], 13);
const mcg = L.markerClusterGroup();
L.tileLayer("https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  className: "map-tiles",
}).addTo(map);

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
  favoriteStations = new Array();
  totalCount = 0;

  constructor(dataUrl, userId = null, isFavoriteMap) {
    this.dataUrl = dataUrl;
    this.userId = userId;
    this.isFavoriteMap = isFavoriteMap;
  }

  async setStations() {
    try {
      const res = await fetch(this.dataUrl);
      if (!res.ok) {
        console.error("Erreur de chargement des données OpenData.")
        return;
      } 

      const rawData = await res.json();
      let opendata = rawData.results;
      this.totalCount = rawData.totalCount;

      if (this.isFavoriteMap) {
        const resFavs = await fetch(`http://localhost:8002/api/favorites/${this.userId}`);
        if (!resFavs.ok) {
          console.error("Erreur de chargement des données favorites.")
          return;  
        }
        this.favoriteStations = (await resFavs.json()).data;
        opendata = opendata.reduce((acc, curr) => {
          const isFavorite = this.favoriteStations.find(favoriteStation => favoriteStation.station_code === curr.stationcode);
          if (isFavorite) {
            acc.push({
              ...isFavorite,
              ...curr
            })
          }
          return acc;
        }, [])
      }

      opendata.map((station) => {
        const coordinates = [station.coordonnees_geo.lat, station.coordonnees_geo.lon];
        const icon = this.isFavoriteMap ? favoriteStationIcon : stationIcon;
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

        mcg.addLayer(marker);
        return marker;
      });
      mcg.addTo(map);
      // debugger;
    } catch (error) {
      console.error('Erreur de chargement des stations:', error);
    }
  }
}

const velybMap = new VelybMap("http://localhost:8004/", userId ? userId : null, isFavoritePage);
velybMap.setStations();
