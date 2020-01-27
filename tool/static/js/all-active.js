$(document).ready(function() {
    // If the checkbox in the header of the table is clicked, check all checkboxes in table
    $("#allActive").click(function() {
        $(".table input:checkbox").prop("checked", $(this).prop("checked"));
    });

});