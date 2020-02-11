
// Making list objects clickable
$(document).ready(function(){
$(document).on('click','.config-list-item', function() {
    $(this).parent().children().removeClass("active");
    $(this).addClass("active");
    document.getElementById('name_new_config').value = $(this).text();
    var configID = $(this).attr('data-cid');
    
// Insert values from Configuration model into inputs
// Checking checkboxes for documents in Configuration
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
            var id_list = data.id_list;
            
            document.getElementById('amount_topics').value = data.topics;
            $("#date_from").val(data.dateFrom)
            $("#date_until").val(data.dateUntil).trigger('change', [ id_list ]);
            
            }
            
            
    });
});

});


