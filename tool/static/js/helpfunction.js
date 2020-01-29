$(document).ready(function(event) { 
    // Show help dialogue if user clicks on help icon
    $('#help_button').click(function() { 
        
        $.blockUI({
            message: $('#help_dialogue'),
            overlayCSS:{cursor:"default"}
            
        });
        $('.blockUI.blockMsg').center();
        
        // Hide dialogue if user clicks "Ok"
        $('#ok').click(function() { 
            $.unblockUI(); 
            event.preventDefault();
            return false; 
        }); 
        
    }); 
    // Place dialogue in the center of the screen
    $.fn.center = function () {
        this.css("position","absolute");
        this.css("top", ($(window).height() - this.height()) / 2+$(window).scrollTop() + "px");
        this.css("left", ( $(window).width() - this.width() ) / 2+$(window).scrollLeft() + "px");
        this.css("border", "5px solid #add8e6")
        this.css("cursor", "default")
        
        return this;
    }
    }); 
