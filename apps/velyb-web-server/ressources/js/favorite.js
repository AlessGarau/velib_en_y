const user_id = document.cookie.split("user_id=")[1];

async function addFavorite(station_code, name) {
    try {
        const data = {
            user_id: user_id,
            station_code: station_code,
            name: name,
            picture: "", // N'est même pas sur la maquette donc pas utilisé mais ok
            name_custom: name
        };

        const res = await axios.post('http://localhost:8002/api/favorites/', data);
        if (res.data.success) {
            console.log(res.data.data);
            window.location.href = "/favorites"
        } else {
            console.error("Erreur lors de l'ajout du favori :", res.data.message);
        }
    } catch (error) {
        console.error("Erreur lors de l'ajout du favori :", error);
    }
}
