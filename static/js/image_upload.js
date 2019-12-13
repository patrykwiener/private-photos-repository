$('#id_image').on('change', function () {
    var fileName = $(this).val();
    if (fileName === "") {
        fileName = "Choose file";
    }
    $(this).next('.custom-file-label').html(fileName);
});

$(document).ready(function () {
    $("#form_id").on("submit", function () {
        $('#upload-btn').html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Uploading...').addClass('disabled');
    });
});