
// Making list objects clickable
$(document).ready(function(){
$(document).on('click','.list-group-item', function() {
    $(this).parent().children().removeClass("active");
    $(this).addClass("active");
    document.getElementById('name_new_config').value = $(this).text();
});

});


