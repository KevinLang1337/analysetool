
$(document).ready(function() { 
 var fileSelect=document.getElementById("file-select-input");
    fileSelect.onchange=function(event){
        event.preventDefault();
        var files = fileSelect.files;
        var formData = new FormData();
        for(var i = 0; i < files.length; i++){
            var file = files[i];
            formData.append('myfiles[]', file, file.name);    
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
    }
})
