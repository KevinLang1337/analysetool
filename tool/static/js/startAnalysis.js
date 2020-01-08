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
            anzahl: $('#amount_topics').val()
        },
        success: function () {
            window.location.href = "../webcrawler/";
        }
    });
}
        