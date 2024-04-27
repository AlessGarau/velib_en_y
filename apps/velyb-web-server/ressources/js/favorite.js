const user_id = document.cookie.split("user_id=")[1];

async function addFavorite(station_code, name) {
    try {
        const data = {
            user_id: user_id,
            station_code: station_code,
            name: name,
            picture: "x", // N'est même pas sur la maquette donc pas utilisé mais ok
            name_custom: name
        };

        const res = await fetch('http://localhost:8002/api/favorites/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const resData = await res.json();
        if (!res.ok) {
            console.error("Erreur lors de l'ajout du favori:", resData.message);
        }
        
        console.log(resData.data);
    } catch (error) {
        console.error("Erreur lors de l'ajout du favori :", error);
    }
}
