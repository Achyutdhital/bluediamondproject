

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
            // Ensure each submenu has a back control for slide navigation
            try {
                var $root = $(menu);
                $root.find('li.hasChild > ul.submenu').each(function(){
                    var $submenu = $(this);
                    if ($submenu.find('> li.back').length === 0) {
                        $submenu.prepend('<li class="back"><a href="#">Back</a></li>');
                    }
                });
            } catch (e) {
                // no-op
            }
            },
            onMenuToggle: function(menu, opened) {
                console.log(opened)
            },
            "menuStyle": "slide"
        });

        // Prevent navigation when tapping parent label in mobile menu; open the submenu instead
        // Works with the plugin's slide style which shows submenu when parent li has class `active`
        $(document).on('click', '.sm_menu_outer .mobile_menu li.hasChild > a', function(e){
            var $li = $(this).parent('li');
            var $submenu = $li.children('ul.submenu');
            if ($submenu.length) {
                e.preventDefault();
                e.stopPropagation();
                // activate this submenu panel
                $li.addClass('active');
            }
        });

        // Handle Back action inside slide submenus
        $(document).on('click', '.sm_menu_outer .mobile_menu li.back > a', function(e){
            e.preventDefault();
            e.stopPropagation();
            var $parentLi = $(this).closest('ul.submenu').closest('li.hasChild');
            $parentLi.removeClass('active');
        });
    })
            