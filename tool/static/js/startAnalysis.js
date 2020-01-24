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
    
  



function startAnalysis() {
    $.blockUI({
        message: $('#spinnerStart'),
        css: {
            border: '5px solid #add8e6',
            width: '25%',
        }
    });

    var filenames = [],
        $activeChk = $('#source_table input:checkbox:checked');
        if ($activeChk.length === 0) {
            alert("Keine Quellen ausgewählt!");
            return;
        }
        $activeChk.each(function() {
            filenames.push( $(this).closest('tr').children().eq(1).text() );
        });
        


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
            filenames: filenames
        },
        success: function () {
            window.location.href = "../ergebnisse/";
        }
    });
}
        