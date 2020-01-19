
$(document).ready(function() { 
 var fileSelect = document.getElementById("file-select-input");
    fileSelect.onchange=function(event){
        event.preventDefault();
        $('#upload-form').submit();
    };
})
