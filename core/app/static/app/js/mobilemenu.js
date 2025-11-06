

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
            "menuStyle": "accordion"
        });
    })*/
    

            
$(document).ready(function() {
        $(".mobile_menu").simpleMobileMenu({
            onMenuLoad: function(menu) {
            // Ensure "Back" control only for slide navigation (not accordion)
            try {
                var $root = $(menu);
                var $wrapper = $root.closest('.sm_menu_outer');
                if ($wrapper.hasClass('slide')) {
                    $root.find('li.hasChild > ul.submenu').each(function(){
                        var $submenu = $(this);
                        if ($submenu.find('> li.back').length === 0) {
                            $submenu.prepend('<li class="back"><a href=\"#\">Back</a></li>');
                        }
                    });
                }
            } catch (e) {
                // no-op
            }
            },
            onMenuToggle: function(menu, opened) {
                console.log(opened)
            },
            "menuStyle": "accordion"
        });

        // Close when clicking outside the drawer (on the dim overlay)
        $(document).on('click', '.sm_menu_outer', function(e){
            if ($(e.target).closest('.mobile_menu').length === 0) {
                $('#sm_menu_ham').removeClass('open');
                $('.sm_menu_outer').removeClass('active');
                $('body').removeClass('mmactive');
            }
        });

        // Close drawer after tapping a LEAF link (no submenu). Do NOT close for parent toggles.
        $(document).on('click', '.sm_menu_outer .mobile_menu a', function(e){
            var $a = $(this);
            var $li = $a.parent('li');
            var isBack = $li.hasClass('back');
            var hasSubmenu = $li.hasClass('hasChild') || $a.siblings('ul.submenu').length > 0;

            if (isBack) {
                // In accordion mode, collapse this submenu instead of closing the drawer
                e.preventDefault();
                e.stopPropagation();
                var $wrapper = $a.closest('.sm_menu_outer');
                var $parentLi = $a.closest('ul.submenu').closest('li.hasChild');
                if ($wrapper.hasClass('accordion')) {
                    $parentLi.children('ul.submenu').slideUp();
                }
                $parentLi.removeClass('active');
                return;
            }

            if (hasSubmenu) {
                // Let the plugin toggle the submenu; don't close the drawer
                return;
            }

            // Leaf link - close the drawer and proceed with navigation
            $('#sm_menu_ham').removeClass('open');
            $('.sm_menu_outer').removeClass('active');
            $('body').removeClass('mmactive');
        });

        // Prevent navigation and slide-open only for slide style (not used now, but kept for future)
        $(document).on('click', '.sm_menu_outer.slide .mobile_menu li.hasChild > a', function(e){
            var $li = $(this).parent('li');
            var $submenu = $li.children('ul.submenu');
            if ($submenu.length) {
                e.preventDefault();
                e.stopPropagation();
                $li.addClass('active');
            }
        });

        // Handle Back action inside submenus (works for both slide and accordion)
        $(document).on('click', '.sm_menu_outer .mobile_menu li.back > a', function(e){
            e.preventDefault();
            e.stopPropagation();
            var $wrapper = $(this).closest('.sm_menu_outer');
            var $parentLi = $(this).closest('ul.submenu').closest('li.hasChild');
            if ($wrapper.hasClass('accordion')) {
                $parentLi.children('ul.submenu').slideUp();
            }
            $parentLi.removeClass('active');
        });
    })
            