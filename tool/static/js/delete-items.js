// Delete Configuration onclick
function deleteConfig(){
    var cid = $('ul li.active').attr("data-cid");
    
    if (typeof cid !== "undefined"){
    
    $.ajax({
        type: 'POST',
        url: '../deleteconfig/',
        data:{ cid: cid
        },
        //Reload window on success
        success: function () {
        $('ul li.active').remove();
        window.location.reload();        
        }
});
}
}

// Delete Table Row and Model Entry of Document when trashcan is clicked
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

// Delete all Documents and Model entries onclick
$(function(){
    $('table').on('click','tr a.deleteAll',function(e){
        e.preventDefault();
        var sourceTable = $(this).parents('tr').parents('thead').parents('table')
        var tableLength = $(sourceTable).prop('rows').length;

        // When table is empty, do nothing
        if(tableLength<=1){
            return false;
        }

        // Ask User if they really want to delete all sources
        $.blockUI({
            message: $('#confirm_delete'),
            overlayCSS: {
                cursor: 'default',
                
            }
            
        });
        $('.blockUI.blockMsg').center();
        // Cancel process if User doesn't want to delete
        $('#cancel_delete_button').click(function() { 
            $.unblockUI(); 
            return false; 
        }); 
        // Continue process
        $('#delete_all_button').click(function() { 
            $.unblockUI();  
        


            var allIDs = [];
        
            // Gather all IDs of documents which are to be deleted
            $(".docIDClass").each(function() {
                allIDs.push($(this).attr("data-did"))
            })
            // Delete all rows from table
            sourceTable.find('tbody').empty();
            // Send IDs to server
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


 

 
 