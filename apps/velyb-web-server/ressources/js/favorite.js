// Already called in map.py
// const user_id = document.cookie.split("user_id=")[1];

async function addFavorite(station_code, name) {
    try {
        const data = {
            user_id: user_id,
            station_code: station_code,
            name: name,
            picture: "", // N'est même pas sur la maquette donc pas utilisé mais ok
            name_custom: name
        };

        const response = await fetch('http://localhost:8002/api/favorites/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const responseData = await response.json();
        
        if (responseData.success) {
            console.log(responseData.data);
            // window.location.href = "/favorites"
        } else {
            console.error("Erreur lors de l'ajout du favori :", responseData.message);
        }
    } catch (error) {
        console.error("Erreur lors de l'ajout du favori :", error);
    }
}
