function calculateDistance() {
    const origin = document.getElementById("origin").value;
    const destination = document.getElementById("destination").value;
    const apikey = "jaihcih"; //тут апи ключа опять
    const url = https / maps.googleapis.com / maps / api / distancematrix / json ?

        origin : { origin }; destination; $; { destination; } key; $; { apikey; };

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.status === "OK") {
                const distance = data.rows[0].elements[0].distance.text;
                document.getElementById("resut").innerText = 'Расстояние между'; $; { origin; } и; $; { destination; } $; { distance; };
            }
            else {
                document.getElementById("result").innerText = "Ошибочка";
            }
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });
}
