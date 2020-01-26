



 $(function(){
    $('table').on('click','tr a.delete',function(e){
       e.preventDefault();
      
     
      var doc_id = $(this).closest("tr").attr("data-did");

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
 
 

 
 