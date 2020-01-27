
// Making list objects clickable
$(document).ready(function(){
$("ul li").click(function() {
    $(this).parent().children().removeClass("active");
    $(this).addClass("active");
});

});


