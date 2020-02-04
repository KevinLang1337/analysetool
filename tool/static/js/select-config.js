
// Making list objects clickable
$(document).ready(function(){
$(document).on('click','.list-group-item', function() {
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
            $Chk = $('#source_table tbody input:checkbox');
            $Chk.each(function() {
            $(this).prop('checked', false);
            var doc_ID = parseInt($(this).closest('tr').attr('data-did'));
            if (id_list.includes(doc_ID)){
                $(this).prop('checked', true);
            }
            })
            document.getElementById('amount_topics').value = data.topics;
            document.getElementById('date_from').value = data.dateFrom;
            document.getElementById('date_until').value = data.dateUntil;
            }
            
            
    });
});

});


