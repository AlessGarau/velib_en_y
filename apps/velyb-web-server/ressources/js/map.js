// TODO - Essayer de garder dernière position en localStorage

import { stations } from "./station.js";

const userId = document.cookie.split("user_id=")[1];

// Set initial view
const map = L.map("map").setView([48.8566, 2.3522], 11);
const mcg = L.markerClusterGroup();
L.tileLayer("https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  className: "map-tiles",
}).addTo(map);

let stationIcon = L.icon({
iconUrl: 'ressources/img/icon-station.svg',
iconSize: [32, 50], 
iconAnchor: [16, 32],
popupAnchor: [0, -32]
});

let favoriteStationIcon = L.icon({
iconUrl: 'ressources/img/favorite-station.svg',
iconSize: [32, 50], 
iconAnchor: [16, 32],
popupAnchor: [0, -32]
});


class VelybMap {
  favoriteStations = new Array();
  opendataRaw = {};
  opendataParsed = []
  isFavoriteMap = window.location.pathname.includes("favorites");
  isListPage = this.isFavoriteMap || window.location.pathname === "/"

  constructor(dataUrl, userId = null) {
    this.dataUrl = dataUrl;
    this.userId = userId;
  }

  async setStations() {
    try {
      const res = await fetch(this.dataUrl);
      if (!res.ok) {
        console.error("Erreur de chargement des données OpenData.")
        return;
      } 

      this.opendataRaw = await res.json();
      this.opendataParsed = [...this.opendataRaw.results];
      
      if (this.userId) {
        const resFavs = await fetch(`http://localhost:8000/bridge/favorites/${this.userId}`);
        if (!resFavs.ok) {
          console.error("Erreur de chargement des données favorites.")
          return;  
        }
        this.favoriteStations = (await resFavs.json()).data;
        if (this.isFavoriteMap) {
          this.opendataParsed = this.opendataParsed.reduce((acc, curr) => {
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
      }

      await this.opendataParsed.map((station) => {
        const coordinates = [station.coordonnees_geo.lat, station.coordonnees_geo.lon];
        const icon = this.isFavoriteMap ? favoriteStationIcon : stationIcon;
        const marker = L.marker(coordinates, {icon : icon}).on('click', (e) => this.scrollToStation(e, station.stationcode));
        marker.bindPopup(`
        <b>${station.name}</b>
        <br/>
        Nombre de vélos disponibles : ${station.numbikesavailable}
        <br/>
        Type : Mécanique : ${station.mechanical}/ Électrique : ${station.ebike}
        <br/>
        Nombre de places libres : ${station.numdocksavailable}
        <br />
        ${
          this.isFavoriteMap ? `<button class="cta-popup delete" onclick="removeFavorite(${station.stationcode}, '${station.name}')">Supprimer ce favori</button>` : 
          this.userId ? `<button class="cta-popup add" onclick="addFavorite(${station.stationcode}, '${station.name}')">Ajouter aux favoris</button>` 
          : `<button class="cta-popup unavailable" onclick="addFavorite(${station.stationcode}, '${station.name}')">Ajouter aux favoris</button>`
        }
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

  scrollToStation(e, stationCode) {
    if (!this.isListPage) return;

    const stationCard = document.getElementById(stationCode);
    const headerCard = document.getElementsByClassName('header-component')[0];
    const sideBar = document.getElementById('sidebar-section')

    stationCard.scrollIntoView(true);
    sideBar.scrollBy({top: -(headerCard.getBoundingClientRect().height + 50), behavior: "smooth"})

    stationCard.classList.add('selected-station-card');
    setTimeout(() => {
      stationCard.classList.remove('selected-station-card');
    }, 4000);
  }
}

export const velybMap = new VelybMap("http://localhost:8000/bridge/cache/", userId ? userId : null);

await velybMap.setStations();
if (velybMap.isListPage) await stations.setStationList(velybMap.opendataParsed, velybMap.favoriteStations, velybMap.isFavoriteMap);
