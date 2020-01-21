$(document).ready(function() { 
    var fileSelect=document.getElementById("file-select-input");
    $(document).on("submit", "#upload-form", function(e){
           e.preventDefault();
           var files = fileSelect.files;
           var formData = new FormData();
           
           for(var i = 0; i < files.length; i++){
               var file = files[i];
               formData.append('newfiles[]', file, file.name);    
           }
           for (var [key, value] of formData.entries()) { 
            console.log("Key: ", key, "Value: ", value);
          }
          
           
           
           $.ajax({
               type: 'POST',
               url: '../konfiguration/',
               action:'post',
               data:formData,
               processData:false,
               contentType:false,
               success: function () {
                   alert("Upload abgeschlossen!");
               }
           });
       })
   })