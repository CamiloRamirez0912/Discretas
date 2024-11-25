document.addEventListener("DOMContentLoaded", () => {
    let map;
    let geocoder;
    let hospitalMarkers = [];
    let accidentMarker;

    // Inicializar el mapa
    const initMap = () => {
        const centerCoords = { lat: 5.544, lng: -73.356 };

        // Crear el mapa
        map = new google.maps.Map(document.getElementById("map"), {
            zoom: 13,
            center: centerCoords,
        });

        // Inicializar el geocodificador
        geocoder = new google.maps.Geocoder();

        // Crear una ventana de información
        const infoWindow = new google.maps.InfoWindow();

        // Agregar los hospitales con íconos personalizados y eventos
        fetch("/api/hospitals")
        .then((response) => response.json())
        .then((hospitals) => {
            hospitals.forEach((hospital) => {
                const iconUrl = hospital.tipo === "hospital"
                    ? "/static/assets/hospital.png"  
                    : "/static/assets/firefighter.png"; 

                const marker = new google.maps.Marker({
                    position: { lat: hospital.lat, lng: hospital.lng },
                    map: map,
                    title: hospital.nombre,
                    icon: {
                        url: iconUrl,
                        scaledSize: new google.maps.Size(30, 30),
                    },
                });

                marker.addListener("mouseover", () => {
                    infoWindow.setContent(hospital.nombre);
                    infoWindow.open(map, marker);
                });

                marker.addListener("mouseout", () => {
                    infoWindow.close();
                });

                hospitalMarkers.push(marker);
            });
        })
        .catch((error) => console.error("Error cargando hospitales:", error));
    };

    // Buscar dirección y marcar el accidente
    const searchAddress = () => {
        const address = document.getElementById("address").value;

        if (!address) {
            alert("Por favor, ingrese una dirección.");
            return;
        }

        geocoder.geocode({ address: address }, (results, status) => {
            if (status === "OK") {
                const location = results[0].geometry.location;

                // Centrar el mapa
                map.setCenter(location);

                // Agregar un marcador para la dirección
                if (accidentMarker) {
                    accidentMarker.setMap(null); // Eliminar el marcador previo si existe
                }
                accidentMarker = new google.maps.Marker({
                    position: location,
                    map: map,
                    title: "Ubicación del accidente",
                    icon: {
                        url: "/static/assets/accident.png", // Ícono del accidente
                        scaledSize: new google.maps.Size(30, 30),
                    },
                });
            } else {
                alert("No se pudo encontrar la dirección: " + status);
            }
        });
    };

    // Asignar evento al botón de búsqueda
    document.getElementById("searchBtn").addEventListener("click", searchAddress);

    // Inicializar el mapa al cargar la página
    initMap();
});
