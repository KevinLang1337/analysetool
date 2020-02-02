$(document).ready(function(){
    $(document).on("submit", "#configForm", function(e){
        e.preventDefault();
        if(buttonIndex==1){
            startAnalysis();
        }
        else if(buttonIndex==2){
            upload_config();
        }
        else return false;
        })
        
    })
    
  


// Start analyzing 
function startAnalysis() {
    // Show dialogue while loading, block UI to prevent User interactions
    $.blockUI({
        message: $('#spinnerStart'),
        css: {
            border: '5px solid #add8e6',
            width: '25%',
        }
    });

    var file_ids = [],
        $activeChk = $('#source_table tbody input:checkbox:checked');
        // If there are no sources selected, show dialogue
        if ($activeChk.length === 0) {
            $.blockUI({
                message: $('#no_sources'),
                css: {
                    border: '5px solid #add8e6',
                    
                }
                
            });
            $('.blockUI.blockMsg').center();

            $('#newTry').click(function() { 
                $.unblockUI(); 
            }); 
            return false;
        }
        // Collect sources in array
        $activeChk.each(function() {
            var doc_ID = $(this).closest('tr').attr('data-did');
            file_ids.push( doc_ID );
            
        });

    // Send values to view
    $.ajax({
        type: 'POST',
        url: '../webcrawler/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            amount: $('#amount_topics').val(),
            date_from: $('#date_from').val(),
            date_until: $('#date_until').val(),
            file_ids: file_ids
        },
        success: function () {
            window.location.href = "../ergebnisse/";
        }
    });
}
        