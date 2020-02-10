
// Saving configurations

function crawlerSaveOrOverwrite() {
    
    var configList = document.getElementById('crawler_config_list');
    $.blockUI({
        message: $('#crawler_dia_save'),
        overlayCSS: { cursor: "default" }

    });
    $('.blockUI.blockMsg').center();

    // Hide dialogue if user cancels saving
    $('#crawler_cancel_save_config_button').off().on('click', function () {
        $.unblockUI();
        
        return false;
    });

    // Save configuration with name from text input
    $('#crawler_save_new_config_form').off().on('submit', function (e) {
        
        e.preventDefault();
        var newConfigName = document.getElementById('crawler_name_new_config').value;
        newConfigName = newConfigName.trim();
        var config_name_exists = $('.crawler-list-item').filter(function () {
            return $(this).text() == newConfigName;
        });
        var urls = [],
        $activeChk = $('#crawler_source_table tbody input:checkbox:checked');
        $activeChk.each(function() {
            var url_id = $(this).closest('tr').attr('data-uid');
            urls.push( url_id );
            
        });
        
        

        // Save configuration, if name does not exist
        if (!config_name_exists.length) {
            
            
            $.ajax({
                type: 'POST',
                url: '../crawlersaveconfig/',
                data:{
                    action: 'post',
                    dataType: 'json',
                    contentType: 'application/json; charset=utf-8',
                    timeout: $('#timeout_crawling').val(),
                    sites: $('#amount_websites').val(),
                    dateFrom: $('#crawler_date_from').val(),
                    dateUntil: $('#crawler_date_until').val(),
                    title: newConfigName,
                    urls: urls
                },
                success: function (data) {
                    if (data.is_valid){
                        
                    var entry = document.createElement('li');
                    $(entry).addClass("list-group-item");
                    $(entry).addClass("crawler-list-item");
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
                message: $('#crawler_dia_overwrite'),
                overlayCSS: { cursor: "default" }

            });
            $('.blockUI.blockMsg').center();

            // Hide dialogue if User cancels overwriting
            $('#crawler_cancel_overwrite_button').off().on('click',function () {
                $.unblockUI();
                
                return false;
            });

            // Overwrite configuration with name from text input
            $('#crawler_confirm_overwrite_button').off().on('click',function () {
                $.ajax({
                    type: 'POST',
                    url: '../crawlersaveconfig/',
                    data:{
                        action: 'post',
                        dataType: 'json',
                        contentType: 'application/json; charset=utf-8',
                        timeout: $('#timeout_crawling').val(),
                        sites: $('#amount_websites').val(),
                        dateFrom: $('#crawler_date_from').val(),
                        dateUntil: $('#crawler_date_until').val(),
                        title: newConfigName,
                        urls: urls
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