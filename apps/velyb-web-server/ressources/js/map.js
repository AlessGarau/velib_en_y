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

class VelybMap {
  favoriteStations = new Array();
  totalCount = 0;

  constructor(dataUrl, userId = null, isFavoriteMap) {
    this.dataUrl = dataUrl;
    this.userId = userId;
    this.isFavoriteMap = isFavoriteMap;
  }

  async set_stations() {
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

    const markers = opendata.map((station) => {
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

      mcg.addLayer(marker);
      return marker;
    });

    mcg.addTo(map);
    // debugger;
  }
}

const velybMap = new VelybMap("http://localhost:8004/", userId ? userId : null, isFavoritePage);
velybMap.set_stations();
