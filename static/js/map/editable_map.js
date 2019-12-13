let map = null;

function initMap() {
    map = new EditableMapManager('map', 'id_latitude', 'id_longitude');
}

function getMarkerPosition() {
    map.getMarkerPosition();
}
