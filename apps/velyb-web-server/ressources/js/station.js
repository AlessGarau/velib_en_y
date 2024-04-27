class Stations {
    stations_per_commune = new Object();
    // clé: nnom de la commune
    // valeur: array avec toutes les stations

    // Code dans la loop 
    // if (!this.stations_per_commune.hasOwnProperty(station.nom_arrondissement_communes)) {
    //     this.stations_per_commune[station.nom_arrondissement_communes] = new Array();
    //   }
    //   this.stations_per_commune[station.nom_arrondissement_communes].push({ station: station, marker: marker });
}

// 1. Fetch toutes les stations 
// 2. Commune de base: Paris
// 
// 3. Loop dans les results du fetch, et créer le html de la station card SI elle est dans la commune spécifiée
// 4. Faire une variable arrondissements_communes qui est un array avec le nom des communes

// À partir de la variable arrondissements_communes, remplir le select

// EventListener du Select => Lance la loop étape 3 avec la nouvelle commune défini