  
function initMap() {
    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        console.log(lat,lng)
        // Do something with the coordinates
        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 12,
            center: { lat, lng },
            disableDefaultUI: true,
        });
        var curr_marker = new google.maps.Marker({
            map: map,
            position: {lat,lng},
            icon: {
                url: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png"
              },
            title: 'Current Location'
        });

        var service = new google.maps.places.PlacesService(map);
        service.nearbySearch({
        location: {lat, lng},
        radius: 3000,
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
            console.log(marker.title,place.geometry.location.lat(),place.geometry.location.lng());
            // Create a new DirectionsService object
            var directionsService = new google.maps.DirectionsService();

            // Create a new DirectionsRenderer object to display the route on the map
            var directionsRenderer = new google.maps.DirectionsRenderer();

            // Attach the DirectionsRenderer object to the map
            directionsRenderer.setMap(map);
            // Attach an event listener to the marker to handle clicks
            marker.addListener('click', function() {
                // Create a new DirectionsRequest object with the start and end locations
                var directionsRequest = {
                origin: {lat,lng},
                destination: this.getPosition(),
                travelMode: 'DRIVING'
                };
                console.log(this.title,this.getPosition());
                // Call the route method on the DirectionsService object to calculate the route
                directionsService.route(directionsRequest, function(response, status) {
                if (status === 'OK') {
                    // Display the route on the map using the DirectionsRenderer object
                    directionsRenderer.setDirections(response);
                } else {
                    // Display an error message if the route calculation failed
                    window.alert('Directions request failed due to ' + status);
                }
                });
                            
            });
            //console.log(marker);
            marker.addListener('click', function() {
                // create a DistanceMatrixService object
                var distanceService = new google.maps.DistanceMatrixService();

                // define the marker location and the user's location
                var markerLocation = this.getPosition();
                var userLocation = {lat, lng};

                // call the Distance Matrix API with the marker and user locations
                distanceService.getDistanceMatrix({
                origins: [userLocation],
                destinations: [markerLocation],
                travelMode: 'DRIVING',
                unitSystem: google.maps.UnitSystem.IMPERIAL,
                }, function(response, status) {
                // parse the JSON response to get the travel time value
                var travelTime = response.rows[0].elements[0].duration.text;

                // display the travel time value on the marker's infowindow or as a separate element on the map
                var infowindow = new google.maps.InfoWindow({
                    content: 'Travel time: ' + travelTime
                });
                infowindow.setPosition(markerLocation)
                infowindow.open(map);
                });
            });
            }
        }
        });

    });
  }  