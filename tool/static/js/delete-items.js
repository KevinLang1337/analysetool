



 $(function(){
    $('table').on('click','tr a.delete',function(e){
       e.preventDefault();
      
     
      var doc_id = [];
      doc_id.push($(this).closest("tr").attr("data-did"));

        $(this).parents('tr').remove();

        $.ajax({
            type: 'POST',
            url: '../delete/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post',
                doc_id:doc_id
            },
            success: function () {
                
            }
        });  
    });
});
 
$(function(){
    $('table').on('click','tr a.deleteAll',function(e){
        e.preventDefault();
        var sourceTable = $(this).parents('tr').parents('thead').parents('table')
        var tableLength = $(sourceTable).prop('rows').length;

        if(tableLength<=1){
            return false;
        }


        $.blockUI({
            message: $('#confirm_delete'),
            css: {
                border: '5px solid #add8e6',
                
            }
            
        });
        $('.blockUI.blockMsg').center();
        
        $('#cancel_delete_button').click(function() { 
            $.unblockUI(); 
            return false; 
        }); 
        $('#delete_all_button').click(function() { 
            $.unblockUI();  
        


            var allIDs = [];
        
            
            $(".docIDClass").each(function() {
                allIDs.push($(this).attr("data-did"))
            })
        
            sourceTable.find('tbody').empty();
        $.ajax({
            type: 'POST',
            url: '../delete/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post',
                doc_id:allIDs
            },
            success: function () {
                
            }
        });  
    });
}); 

    })


 

 
 