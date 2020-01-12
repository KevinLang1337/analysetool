
$(document).ready(function() { 
 
    $('#upload_config_button').on("click",function(e) {
        e.preventDefault(); 
        const customBtn = document.getElementById("upload_config_button");
        const realFileBtn=document.getElementById("source_upload_config");
        const uploadTxt=document.getElementById("upload_text");

        customBtn.addEventListener("click", function(){
            realFileBtn.click();
        })
        realFileBtn.addEventListener("change", function(){
            if(realFileBtn.value){
                uploadTxt.placeholder=realFileBtn.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
            }
        })
        return false;
        });
})
