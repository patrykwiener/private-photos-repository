let originalHeight = $('#imageOriginalHeight').val();
let image = $('#img_container');

function map_faces() {
    let elements = image.children();
    for (let element of elements) {
        map_face_to_image(element);
    }
}

function map_face_to_image(rect) {
    if (rect.id.search('face') !== -1) {
        let currentHeight = image.height();
        let currentWidth = image.width();
        let factor = currentHeight / originalHeight;
        let original_coordinates = rect.getAttribute('data-value');
        let coordinates = original_coordinates.substring(1, original_coordinates.length - 1).split(", ");
        let top = coordinates[0];
        let left = coordinates[3];
        let width = coordinates[1] - coordinates[3];
        let height = coordinates[2] - coordinates[0];
        let coordTop = top * factor - 5;
        let coordLeft = left * factor - 5;
        let coordWidth = width * factor + 10;
        let coordHeight = height * factor + 10;

        rect.style.top = ((coordTop >= 0) ? coordTop : 0) + "px";
        rect.style.left = ((coordLeft >= 0) ? coordLeft : 0) + "px";
        rect.style.width = ((coordLeft + coordWidth > currentWidth) ? currentWidth : coordWidth) + "px";
        rect.style.height = ((coordTop + coordHeight > currentHeight) ? currentHeight : coordHeight) + "px";
    }
}

new ResizeSensor(jQuery(image), function () {
    map_faces();
});