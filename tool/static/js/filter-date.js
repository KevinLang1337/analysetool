$(function () {
    $(".date-field").off().on('change',function (event, param1) { 
        var doc_ID = []
        if (typeof param1 != 'undefined'){
         doc_ID = param1;
        }
        
        
        inputdate = new Date(this.value);
        if(!isNaN(inputdate.getTime()))
        {
            var month = inputdate.getMonth()+1;
            var date = inputdate.getFullYear() + "-" + month + "-" + inputdate.getDate();
            
            $.ajax({
                type: 'POST',
                url: '../filterdate/',
                data:{
                    action: 'post',
                    dataType: 'json',
                    contentType: 'application/json; charset=utf-8',
                    date: date
                },
                success: function (data) {
                if (typeof doc_ID == 'undefined'){
                $activeChk = $('#source_table tbody input:checkbox:checked');
                $activeChk.each(function() {
                var this_ID = parseInt($(this).closest('tr').attr('data-did'));
                    doc_ID.push(this_ID)
                    })
                }
                    $sourceTable = $('#source_table tbody');
                    $sourceTable.empty();
                    $.each(data, function(index, item) {
                    var date = item['dateField'];
                    var dateConverted = date.split("-");
                    var date = (dateConverted[2]+"."+dateConverted[1]+"."+dateConverted[0]);
                    $("#source_table tbody").prepend(
                        "<tr class = 'docIDClass' data-did=" + item['id'] +">" + "<td><input type='checkbox' scope='row' /></td>" +
                        "<td>"+ item['title'] + "</td>" + "<td>"+ 
                        date + "</td>" +
                        "<td>"+ item['extension'] + "</td>"  +
                        "<td><a class='delete' href=''><span class='glyphicon glyphicon-trash'></span></a> </span><td>" +
                        "<td style='display:none'>" + item['id'] +"</td>" +
                        "</tr>"
              
                      );

                    })
                    $Chk = $('#source_table tbody input:checkbox');
                    $Chk.each(function() {
                    var this_ID = parseInt($(this).closest('tr').attr('data-did'));
                   if (doc_ID.includes(this_ID)){
                    $(this).prop('checked', true);
            }
            })
                    }
                    
                    
            });
        }
    })
})