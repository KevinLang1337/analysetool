$(document).ready(function() { 
 
    $('#help_button').click(function() { 
        $.blockUI({
            message: $('#help_dialogue'),
            css: {
                border: '5px solid #add8e6',
                
            }
            
        });
        $('.blockUI.blockMsg').center();
        
        $('#ok').click(function() { 
            $.unblockUI(); 
            return false; 
        }); 
 
    }); 

    $.fn.center = function () {
        this.css("position","absolute");
        this.css("top", ($(window).height() - this.height()) / 2+$(window).scrollTop() + "px");
        this.css("left", ( $(window).width() - this.width() ) / 2+$(window).scrollLeft() + "px");
        return this;
    }
    }); 
