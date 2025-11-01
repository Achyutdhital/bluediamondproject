

/*            
    $(document).ready(function() {
        $(".mobile_menu").simpleMobileMenu({
            onMenuLoad: function(menu) {
                console.log(menu)
                console.log("menu loaded")
            },
            onMenuToggle: function(menu, opened) {
                console.log(opened)
            },
            "menuStyle": "slide"
        });
    })*/
    

            
$(document).ready(function() {
        $(".mobile_menu").simpleMobileMenu({
            onMenuLoad: function(menu) {
            
            },
            onMenuToggle: function(menu, opened) {
                console.log(opened)
            },
            "menuStyle": "slide"
        });
    })
            