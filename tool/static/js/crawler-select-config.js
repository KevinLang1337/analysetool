// Making list objects clickable
$(document).ready(function(){
    $(document).on('click','.crawler-list-item', function() {
        $(this).parent().children().removeClass("active");
        $(this).addClass("active");
        document.getElementById('crawler_name_new_config').value = $(this).text();
        var configID = $(this).attr('data-cid');
        
    // Insert values from Configuration model into inputs
    // Checking checkboxes for documents in Configuration
        $.ajax({
            type: 'GET',
            url: '../crawlerselectconfig/',
            data:{
                action: 'get',
                dataType: 'json',
                contentType: 'application/json; charset=utf-8',
                configID: configID
            },
            success: function (data) {
                var id_list = data.id_list;
                $Chk = $('#crawler_source_table tbody input:checkbox');
                $Chk.each(function() {
                $(this).prop('checked', false);
                var url_ID = parseInt($(this).closest('tr').attr('data-uid'));
                if (id_list.includes(url_ID)){
                    $(this).prop('checked', true);
                }
                })
                document.getElementById('amount_websites').value = data.sites;
                document.getElementById('timeout_crawling').value = data.timeout;
                document.getElementById('crawler_date_from').value = data.dateFrom;
                document.getElementById('crawler_date_until').value = data.dateUntil;
                }
                
                
        });
    });
    
    });