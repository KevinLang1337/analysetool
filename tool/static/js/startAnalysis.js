$(document).ready(function(){
    $(document).on ('submit', '#startButtonFormID',function(e){
        e.preventDefault();
        $.blockUI({
            message: $('#spinnerStart'),
            css: {
                border: '5px solid #add8e6',
                width: '25%',
            }
        });
                $.ajax({
                type:'GET',
                url:'../webcrawler',
                success:function(){
                    window.location.href="../webcrawler"
                }
            })
     
    
    })
    
    })
  


        