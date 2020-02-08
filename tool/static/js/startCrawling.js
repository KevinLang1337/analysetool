$(document).ready(function(){
    $(document).on("submit", "#crawlingButtonFormID", function(e){
        e.preventDefault();
        
            startCrawling();
    
        })
        
    })

    // Start analyzing 
function startCrawling() {
    // Show dialogue while loading, block UI to prevent User interactions
    $.blockUI({
        message: $('#spinnerCrawl'),
        css: {
            border: '5px solid #add8e6',
            width: '25%',
        }
    });

    var url_ids = [],
        $activeChk = $('#crawler_source_table tbody input:checkbox:checked');
        // If there are no sources selected, show dialogue
        if ($activeChk.length === 0) {
            $.blockUI({
                message: $('#no_urls'),
                css: {
                    border: '5px solid #add8e6',
                    
                }
                
            });
            $('.blockUI.blockMsg').center();

            $('#crawler_newTry').click(function() { 
                $.unblockUI(); 
            }); 
            return false;
        }
        // Collect sources in array
        $activeChk.each(function() {
            var url_id = $(this).closest('tr').attr('data-uid');
            url_ids.push( url_id );
            
        });

    // Send values to view
    $.ajax({
        type: 'POST',
        url: '../startcrawl/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            timeout_crawling: $('#timeout_crawling').val(),
            amount: $('#amount_websites').val(),
            date_from: $('#crawler_date_from').val(),
            date_until: $('#crawler_date_until').val(),
            url_ids: url_ids
        },
        success: function () {
            window.location.href = "../konfiguration/";
        }
    });
}