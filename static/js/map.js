var marker = null;
var map = null;

function getMarkerPosition() {
    var lat = null;
    var lng = null;
    if (marker) {
        lat = marker.position.lat().toPrecision(9);
        lng = marker.position.lng().toPrecision(9);
        lat = parseFloat(lat).toFixed(6);
        lng = parseFloat(lng).toFixed(6);
    }
    document.getElementById('id_latitude').value = lat;
    document.getElementById('id_longitude').value = lng;
}

