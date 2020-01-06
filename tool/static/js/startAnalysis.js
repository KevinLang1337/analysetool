$(document).ready(function(){
    $(document).on ('submit', '#crawlingButtonFormID',function(e){
        e.preventDefault();
        $.blockUI({
            message: $('#spinner'),
            css: {
                border: '5px solid #add8e6',
                width: '25%',
            }
        });
                $.ajax({
                type:'GET',
                url:'../konfiguration',
                success:function(){
                    window.location.href="../konfiguration"
                }
            })
     
    
    })
    
    })
  


        