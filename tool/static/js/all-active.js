$(document).ready(function() {

    $("#allActive").click(function() {
        $(".table input:checkbox").prop("checked", $(this).prop("checked"));
    });

});