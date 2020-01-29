// Saving configurations

function saveOrOverwrite(event) {
    var configList = document.getElementById('config_list');
    $.blockUI({
        message: $('#dia_save'),
        overlayCSS: { cursor: "default" }

    });
    $('.blockUI.blockMsg').center();

    // Hide dialogue if user cancels saving
    $('#cancel_save_config_button').click(function () {
        event.preventDefault();
        $.unblockUI();
        return false;
    });

    // Save configuration with name from text input
    $('#save_config_button').click(function () {
        var newConfigName = document.getElementById('name_new_config').value;
        var config_name_exists = $('.list-group-item').filter(function () {
            return $(this).text() == newConfigName;
        });
        

        // TODO: Save configuration, if name does not exist
        if (!config_name_exists.length) {

            var entry = document.createElement('li');

            entry.innerHTML = newConfigName;
            $(entry).addClass("list-group-item");
            configList.appendChild(entry);
            $.unblockUI();
            event.preventDefault();
            return false;
        }

        else if (config_name_exists.length) { // Show new dialogue, if name already exists
            alert(config_name_exists.text());
            $.blockUI({
                message: $('#dia_overwrite'),
                overlayCSS: { cursor: "default" }

            });
            $('.blockUI.blockMsg').center();

            // Hide dialogue if User cancels overwriting
            $('#cancel_overwrite_button').click(function (event) {
                $.unblockUI();
                event.preventDefault();
                return false;
            });

            // Overwrite configuration with name from text input
            $('#confirm_overwrite_button').click(function () {
                $.unblockUI();
                event.preventDefault();
                return false;
            });
            event.preventDefault();
            return false;
        }
        
        // TODO: Ajax call to server
        


    });
    
}