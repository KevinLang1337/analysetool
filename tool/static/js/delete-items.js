// Delete Configuration onclick
function deleteConfig(URLaddress){
    var cid = $('ul li.active').attr("data-cid");
    if (typeof cid !== "undefined"){
    
    $.ajax({
        type: 'POST',
        url: URLaddress,
        data:{ cid: cid
        },
        //Reload window on success
        success: function () {
        $('ul li.active').remove();
               
        }
});
}
}


// Delete all URLs and their Model entries onclick
$(function(){
    $('#crawler_source_table').on('click','tr a.deleteAll',function(e){
        e.preventDefault();
        var sourceTable = $(this).parents('tr').parents('thead').parents('table')
        var tableLength = $(sourceTable).prop('rows').length;

        // When table is empty, do nothing
        if(tableLength<=1){
            return false;
        }

        // Ask User if they really want to delete all sources
        $.blockUI({
            message: $('#confirm_delete_urls'),
            overlayCSS: {
                cursor: 'default',
                
            }
            
        });
        $('.blockUI.blockMsg').center();
        // Cancel process if User doesn't want to delete
        $('#cancel_delete_urls_button').click(function() { 
            $.unblockUI(); 
            return false; 
        }); 
        // Continue process
        $('#delete_all_urls_button').click(function() { 
            $.unblockUI();  
        


            var allIDs = [];
        
            // Gather all IDs of documents which are to be deleted
            $(".docIDClass").each(function() {
                allIDs.push($(this).attr("data-uid"))
            })
            // Delete all rows from table
            sourceTable.find('tbody').empty();
            // Send IDs to server
        $.ajax({
            type: 'POST',
            url: '../deletecrawlersource/',
            data:{
                action: 'post',
                url_id:allIDs
            },
            success: function (data) {
                document.getElementById('websites_in_dir').innerHTML = data.number_urls;
            }
        });  
    });
}); 

// Delete Table Row and Model Entry of URL when trashcan is clicked
$(function(){
    $('#crawler_source_table').on('click','tr a.delete',function(e){
       e.preventDefault();
      
     
      var url_id = [];
      url_id.push($(this).closest("tr").attr("data-uid"));

      $(this).parents('tr').remove();

        $.ajax({
            type: 'POST',
            url: '../deletecrawlersource/',
            data:{
                action: 'post',
                url_id:url_id
            },
            success: function (data) {
                document.getElementById('websites_in_dir').innerHTML = data.number_urls;
                
            }
        });  
    });
});



// Delete Table Row and Model Entry of Document when trashcan is clicked
 $(function(){
    $('#source_table').on('click','tr a.delete',function(e){
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
            success: function (data) {
                var earliestDate = "";
                var latestDate = "";
                if (data.earliest_doc != ""){
                    var dateConverted = data.earliest_doc.split("-");
                     earliestDate = (dateConverted[2]+"."+dateConverted[1]+"."+dateConverted[0]);
                    }
                    if (data.latest_doc != ""){
                    dateConverted = data.latest_doc.split("-");
                     latestDate = (dateConverted[2]+"."+dateConverted[1]+"."+dateConverted[0]);
                    }
                    document.getElementById('docs_in_dir').innerHTML = data.number_docs;
                    document.getElementById('earliest_doc_in_dir').innerHTML = earliestDate;
                    document.getElementById('latest_doc_in_dir').innerHTML = latestDate;
            }
        });  
    });
});

// Delete all Documents and Model entries onclick
$(function(){
    $('#source_table').on('click','tr a.deleteAll',function(e){
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
            success: function (data) {
                var earliestDate = "";
                var latestDate = "";
                if (data.earliest_doc != ""){
                var dateConverted = data.earliest_doc.split("-");
                 earliestDate = (dateConverted[2]+"."+dateConverted[1]+"."+dateConverted[0]);
                }
                if (data.latest_doc != ""){
                dateConverted = data.latest_doc.split("-");
                 latestDate = (dateConverted[2]+"."+dateConverted[1]+"."+dateConverted[0]);
                }
                document.getElementById('docs_in_dir').innerHTML = data.number_docs;
                document.getElementById('earliest_doc_in_dir').innerHTML = earliestDate;
                document.getElementById('latest_doc_in_dir').innerHTML = latestDate;
            }
        });  
    });
}); 

    })


 

 
})