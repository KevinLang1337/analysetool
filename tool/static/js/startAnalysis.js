$(document).ready(function(){
    $(document).on("submit", "#configForm", function(e){
        e.preventDefault();
        if(buttonIndex==1){
            startAnalysis();
        }
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
    $.ajax({
        type: 'POST',
        url: '../webcrawler/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post',
            amount: $('#amount_topics').val(),
            date_from: $('#date_from').val(),
            date_until: $('#date_until').val()
        },
        success: function () {
            window.location.href = "../ergebnisse/";
        }
    });
}
        