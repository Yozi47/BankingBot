$(document).ready(function() {
    // Check if geolocation is supported by the browser
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            // Get the user's current latitude and longitude
            var userLat = position.coords.latitude;
            var userLng = position.coords.longitude;

            // Send a request to the Google Places API to get nearby bank locations
            var url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + userLat + ',' + userLng + '&radius=10000&keyword=bank&key=AIzaSyD9oGLBRK6S_J2Kd6ejd8M-jll38MGnS-I';
            $.getJSON(url, function(result) {
                // Loop through the results and display them on the page
                $.each(result.results, function(index, place) {
                    var name = place.name;
                    var address = place.vicinity;
                    var lat = place.geometry.location.lat;
                    var lng = place.geometry.location.lng;
                    var html = '<div>' + name + ': ' + address + '</div>';
                    $('#locations').append(html);

                    // Add a marker to the map for each location
                    var marker = new google.maps.Marker({
                        position: {lat: lat, lng: lng},
                        map: map,
                        title: name
                    });
                });
            });
        });
    } else {
        alert('Geolocation is not supported by your browser.');
    }
});
