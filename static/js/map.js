  
function initMap() {
    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        // Do something with the coordinates
        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 8,
            center: { lat, lng },
            disableDefaultUI: true,
        });

        var service = new google.maps.places.PlacesService(map);
        service.nearbySearch({
        location: {lat, lng},
        radius: 500,
        type: "bank"
        }, 
        function(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            for (var i = 0; i < results.length; i++) {
            var place = results[i];
            // Add a marker to the map for each bank found
            var marker = new google.maps.Marker({
                map: map,
                position: place.geometry.location,
                title: place.name
            });
            }
        }
        });
        console.log(service.status)
    });
  }  