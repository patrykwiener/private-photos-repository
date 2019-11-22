var marker = null;

function initMap() {
    var lat = document.getElementById('id_latitude').value;
    var lng = document.getElementById('id_longitude').value;
    var placeMarker = true;
    var zoom = 9;
    if (lat === "" || lng === "") {
        lat = 50.3785;
        lng = 14.9706;
        placeMarker = false;
        zoom = 4;
    }
    var position = {lat: parseFloat(lat), lng: parseFloat(lng)};
    var map = new google.maps.Map(document.getElementById('map'), {
        center: position,
        zoom: zoom,
        streetViewControl: false
    });
    if (placeMarker) {
        placeMarkerAndPanTo(position, map);
    }
    map.addListener('click', function (e) {
        placeMarkerAndPanTo(e.latLng, map);
    });
}

function placeMarkerAndPanTo(position, map) {
    if (marker) {
        marker.setPosition(position);
    } else {
        marker = new google.maps.Marker({
            position: position,
            map: map,
            draggable: true
        });
    }
    map.panTo(position);
}

function getMarkerPosition() {
    if (marker) {
        var lat = marker.position.lat().toPrecision(9);
        var lng = marker.position.lng().toPrecision(9);
        lat = parseFloat(lat).toFixed(6);
        lng = parseFloat(lng).toFixed(6);
        document.getElementById('id_latitude').value = lat;
        document.getElementById('id_longitude').value = lng;
    }
}