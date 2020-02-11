$(function () {
    $("#url_to_table_button").off().on('click', function () { 
      


    
    $.blockUI({
        message: $('#dia_add_url'),
        overlayCSS: { cursor: "default" }

    });
    $('.blockUI.blockMsg').center();

    // Hide dialogue if user cancels saving
    $('#cancel_add_url_button').off().on('click', function () {
        $.unblockUI();
        return false;
    });

    // Save configuration with name from text input
    $('#dia_save_url').off().on('submit', function (e) {
        e.preventDefault();
        var newURLName = document.getElementById('new_url').value;
        newURLName = newURLName.trim();
        var url_exists = $('.url-list-item').filter(function () {
            return $(this).text() == newURLName;
        });
        
        

        // Save configuration, if name does not exist
        if (!url_exists.length) {

            
            $.ajax({
                type: 'POST',
                url: '../saveurl/',
                data:{
                    action: 'post',
                    dataType: 'json',
                    contentType: 'application/json; charset=utf-8',
                    title: newURLName,
                    
                },
                success: function (data) {
                    if (data.is_valid) {
                        document.getElementById('websites_in_dir').innerHTML = data.number_urls;
                        
                        $("#crawler_source_table tbody").prepend(
                          "<tr class = 'docIDClass' data-uid=" + data.id +">" + "<td><input type='checkbox' scope='row' /></td>" +
                          "<td class = 'url-list-item'>"+ data.title + "</td>" + 
                          "<td><a class='delete' href=''><span class='glyphicon glyphicon-trash'></span></a> </span><td>" +
                          "</tr>"
                          
                        );
                      }
                    $.unblockUI(); 
                    return false;
                }
            });
            
            return false;
        }

        else if (url_exists.length) { // Show new dialogue, if name already exists
            
            $.blockUI({
                message: $('#dia_url_exists'),
                overlayCSS: { cursor: "default" }

            });
            $('.blockUI.blockMsg').center();

            // Hide dialogue if User cancels overwriting
            $('#cancel_url_exists_button').off().on('click',function () {
                $.unblockUI();
                return false;
            });

        
            
        }
        
        
        $(this).off('click'); 
        return false;


    });
    event.preventDefault();
    return false;
})
})
 




    
