
// Making list objects clickable
$(document).ready(function(){
$(document).on('click','.list-group-item', function() {
    $(this).parent().children().removeClass("active");
    $(this).addClass("active");
    document.getElementById('name_new_config').value = $(this).text();
    var configID = $(this).attr('data-cid');
    

    $.ajax({
        type: 'GET',
        url: '../selectconfig/',
        data:{
            action: 'get',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            configID: configID
        },
        success: function (data) {
            
            document.getElementById('amount_topics').value = data.topics;
            document.getElementById('date_from').value = data.dateFrom;
            document.getElementById('date_until').value = data.dateUntil;
            }
            
            
    });
});

});


