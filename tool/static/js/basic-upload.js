$(function () {
  $(".js-upload-photos").click(function () {
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
    done: function (e, data) {
      if (data.result.is_valid) {
        $("#source_table tbody").prepend(
          "<tr data-did=" + data.result.id +">" + "<td><input type='checkbox' scope='row' /></td>" +
          "<td>"+ data.result.name + "</td>" + "<td>"+ 
          "" + "</td>" +
          "<td>"+ data.result.extension + "</td>"  +
          "<td><a class='delete' href=''><span class='glyphicon glyphicon-trash'></span></a> </span><td>" +
          "<td style='display:none'>" + data.result.id +"</td>" +
          "</tr>"

          
        );
      }
    }
  });
  
  });