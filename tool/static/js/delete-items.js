



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
        var allIDs = [];
        
        var sourceTable = $(this).parents('tr').parents('thead').parents('table')
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

    })


 

 
 