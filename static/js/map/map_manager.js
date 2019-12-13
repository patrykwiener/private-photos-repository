class MapManger {

    ZOOM = 9;
    DEFAULT_COORDS = {
        lat: 50.3785,
        lng: 14.9706,
    };

    constructor(map_id, lat_element_id, lng_element_id) {
        this.map = new google.maps.Map(document.getElementById(map_id), {
            streetViewControl: false,
            zoom: this.ZOOM,
        });
        this.position = this.getPosition(lat_element_id, lng_element_id);
        this.map.panTo(this.position);
        this.marker = null;
    }

    placeMarker() {
        if (this.marker) {
            this.marker.setPosition(this.position);
        } else {
            this.createMarker();
        }
    }

    createMarker() {
        throw new Error('Method createMarker has to be implemented!');
    }

    getPosition(lat_element_id, lng_element_id) {
        const lat_element = document.getElementById(lat_element_id);
        const lng_element = document.getElementById(lng_element_id);
        let lat = lat_element.value;
        let lng = lng_element.value;
        if (lat === "" || lng === "") {
            lat = this.DEFAULT_COORDS.lat;
            lng = this.DEFAULT_COORDS.lng;
        }
        return {
            lat: parseFloat(lat),
            lng: parseFloat(lng),
        };
    }
}


class NonEditableMapManager extends MapManger {

    constructor(map_id, lat_element_id, lng_element_id) {
        super(map_id, lat_element_id, lng_element_id);
        this.placeMarker();
    }

    createMarker() {
        this.marker = new google.maps.Marker({
            position: this.position,
            map: this.map,
        });
    }

}

class EditableMapManager extends MapManger {

    ZOOM_WITHOUT_MARKER = 4;

    constructor(map_id, lat_element_id, lng_element_id) {
        super(map_id, lat_element_id, lng_element_id);

        this.lat_element_id = lat_element_id;
        this.lng_element_id = lng_element_id;

        if (this.DEFAULT_COORDS.lat === this.position.lat && this.DEFAULT_COORDS.lng === this.position.lng) {
            this.map.zoom = this.ZOOM_WITHOUT_MARKER;
        } else {
            this.placeMarker();
        }

        const that = this;
        this.map.addListener('click', function (event) {
            that.onAddNewMarker(event);
        });
    }

    onAddNewMarker(event) {
        this.position = event.latLng;
        this.map.panTo(this.position);
        this.placeMarker()
    }


    removeMarker() {
        this.marker.setMap(null);
        this.marker = null;
    }

    createMarker() {
        this.marker = new google.maps.Marker({
            position: this.position,
            map: this.map,
            draggable: true,
        });
        const that = this;
        this.marker.addListener('rightclick', function () {
            that.removeMarker();
        });
    }

    getMarkerPosition() {
        let lat = null;
        let lng = null;
        if (this.marker) {
            lat = this.marker.position.lat().toPrecision(9);
            lng = this.marker.position.lng().toPrecision(9);
            lat = parseFloat(lat).toFixed(6);
            lng = parseFloat(lng).toFixed(6);
        }
        document.getElementById(this.lat_element_id).value = lat;
        document.getElementById(this.lng_element_id).value = lng;
    }
}
