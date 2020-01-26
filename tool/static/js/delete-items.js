



 $(function(){
    $('table').on('click','tr a.delete',function(e){
       e.preventDefault();
      
      var filename;
      var title = $(this).closest('tr').children().eq(1).text();
      var extension = $(this).closest('tr').children().eq(3).text();
        filename=title+extension;
        $(this).parents('tr').remove();

        $.ajax({
            type: 'POST',
            url: '../delete/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post',
                filename:filename
            },
            success: function () {
                
            }
        });  
    });
});
 
 

 
 