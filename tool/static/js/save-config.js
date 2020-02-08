// Saving configurations

function saveOrOverwrite() {
    var configList = document.getElementById('config_list');
    $.blockUI({
        message: $('#dia_save'),
        overlayCSS: { cursor: "default" }

    });
    $('.blockUI.blockMsg').center();

    // Hide dialogue if user cancels saving
    $('#cancel_save_config_button').off().on('click', function () {
        $.unblockUI();
        
        return false;
    });

    // Save configuration with name from text input
    $('#save_new_config_form').off().on('submit', function (e) {
        e.preventDefault();
        var newConfigName = document.getElementById('name_new_config').value;
        newConfigName = newConfigName.trim();
        var config_name_exists = $('.config-list-item').filter(function () {
            return $(this).text() == newConfigName;
        });
        var documents = [],
        $activeChk = $('#source_table tbody input:checkbox:checked');
        $activeChk.each(function() {
            var doc_ID = $(this).closest('tr').attr('data-did');
            documents.push( doc_ID );
            
        });
        
        

        // Save configuration, if name does not exist
        if (!config_name_exists.length) {

            
            $.ajax({
                type: 'POST',
                url: '../saveconfig/',
                data:{
                    action: 'post',
                    dataType: 'json',
                    contentType: 'application/json; charset=utf-8',
                    topics: $('#amount_topics').val(),
                    dateFrom: $('#date_from').val(),
                    dateUntil: $('#date_until').val(),
                    title: newConfigName,
                    documents: documents
                },
                success: function (data) {
                    if (data.is_valid){
                    var entry = document.createElement('li');
                    $(entry).addClass("list-group-item");
                    $(entry).addClass("config-list-item");
                    $(entry).attr('data-cid', data.id);
                    entry.innerHTML = data.title
                    configList.appendChild(entry);
                    }
                    $.unblockUI();
                    
                    return false;;
                }
            });
            
            
            return false;
        }

        else if (config_name_exists.length) { // Show new dialogue, if name already exists
            
            $.blockUI({
                message: $('#dia_overwrite'),
                overlayCSS: { cursor: "default" }

            });
            $('.blockUI.blockMsg').center();

            // Hide dialogue if User cancels overwriting
            $('#cancel_overwrite_button').off().on('click',function () {
                $.unblockUI();
                
                return false;
            });

            // Overwrite configuration with name from text input
            $('#confirm_overwrite_button').off().on('click',function () {
                $.ajax({
                    type: 'POST',
                    url: '../saveconfig/',
                    data:{
                        action: 'post',
                        dataType: 'json',
                        contentType: 'application/json; charset=utf-8',
                        topics: $('#amount_topics').val(),
                        dateFrom: $('#date_from').val(),
                        dateUntil: $('#date_until').val(),
                        title: newConfigName,
                        documents: documents
                    },
                    success: function () {
                        $.unblockUI();
                        
                        return false;;
                    }
                });
                
               
                return false;
            });
            
            return false;
        }
        
        
        


    });
    
}