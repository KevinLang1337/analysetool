// Saving configurations

function saveOrOverwrite(){
    $.blockUI({
        message: $('#dia_save'),
        overlayCSS:{cursor:"default"}
        
    });
    $('.blockUI.blockMsg').center();
    
    // Hide dialogue if user cancels saving
    $('#cancel_save_config_button').click(function() { 
        $.unblockUI(); 
        return false; 
    }); 

    // Save configuration with name from text input
    $('#save_config_button').click(function() { 
    
    // TODO: Save configuration, if name does not exist

        // Show new dialogue, if name already exists
        $.blockUI({
            message: $('#dia_overwrite'),
            overlayCSS:{cursor:"default"}
            
        });
        $('.blockUI.blockMsg').center();
        
        // Hide dialogue if User cancels overwriting
        $('#cancel_overwrite_button').click(function() { 
            $.unblockUI(); 
            return false; 
        }); 

        // Overwrite configuration with name from text input
        $('#confirm_overwrite_button').click(function() { 
            $.unblockUI(); 
            return false; 
        }); 
        return false;
         
    }); 
    return false;
}
