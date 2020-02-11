$(function () {
  $(".js-upload-docs").click(function () { 
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,  /* 1. SEND THE FILES ONE BY ONE */
    start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
      $("#modal-progress").modal("show");
    },
    stop: function (e) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
      $("#modal-progress").modal("hide");
    },
    progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },
    // Add uploaded files to table
    done: function (e, data) {
      if (data.result.is_valid) {
        var dateConverted = data.result.date.split("-");
        var date = (dateConverted[2]+"."+dateConverted[1]+"."+dateConverted[0]);
        $("#source_table tbody").prepend(
          "<tr class = 'docIDClass' data-did=" + data.result.id +">" + "<td><input type='checkbox' scope='row' /></td>" +
          "<td>"+ data.result.name + "</td>" + "<td>"+ 
          date + "</td>" +
          "<td>"+ data.result.extension + "</td>"  +
          "<td><a class='delete' href=''><span class='glyphicon glyphicon-trash'></span></a> </span><td>" +
          "<td style='display:none'>" + data.result.id +"</td>" +
          "</tr>"

          
        );
        var earliestDate = "";
        var latestDate = "";
        if (data.result.earliest_doc != ""){
         dateConverted = data.result.earliest_doc.split("-");
         earliestDate = (dateConverted[2]+"."+dateConverted[1]+"."+dateConverted[0]);
        }
        if (data.result.latest_doc != ""){
        dateConverted = data.result.latest_doc.split("-");
         latestDate = (dateConverted[2]+"."+dateConverted[1]+"."+dateConverted[0]);
        }
        document.getElementById('docs_in_dir').innerHTML = data.result.number_docs;
        document.getElementById('earliest_doc_in_dir').innerHTML = earliestDate;
        document.getElementById('latest_doc_in_dir').innerHTML = latestDate;
      }
    }
  });
  
  });