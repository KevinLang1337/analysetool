$(function () {
    $(".date-field").off().on('change',function (event, param1) { 
        var doc_ID = []
        if (typeof param1 != 'undefined'){
         doc_ID = param1;
        }
         var inputdateFrom = document.getElementById('date_from').value
        var inputdateUntil = document.getElementById('date_until').value

        if (inputdateUntil != ""){
            var dateUntil = new Date(inputdateUntil);
            
            if(!isNaN(dateUntil.getTime()))
            {
                var monthUntil = dateUntil.getMonth()+1;
                inputdateUntil = dateUntil.getFullYear() + "-" + monthUntil + "-" + dateUntil.getDate();
            }
        } 
        
        if (inputdateFrom != ""){
        var dateFrom = new Date(inputdateFrom);
        
        if(!isNaN(dateFrom.getTime()))
        {
            var monthFrom = dateFrom.getMonth()+1;
            inputdateFrom = dateFrom.getFullYear() + "-" + monthFrom + "-" + dateFrom.getDate();
        }
    } 
            $.ajax({
                type: 'POST',
                url: '../filterdate/',
                data:{
                    action: 'post',
                    dataType: 'json',
                    contentType: 'application/json; charset=utf-8',
                    dateFrom: inputdateFrom,
                    dateUntil: inputdateUntil
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
        
    })
})