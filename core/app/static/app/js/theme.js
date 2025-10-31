(function($) {

    "use strict";

    

    var navbar=$('.header_menu, .middle_menu_area, .header_white_menu');

    var nav_offset_top = $('.header_menu, .middle_menu_area, .header_white_menu').offset().top + 60;

    /*-------------------------------------------------------------------------------

      Navbar 

    -------------------------------------------------------------------------------*/

    navbar.affix({

      offset: {

        top: nav_offset_top,

      }

    });


    navbar.on('affix.bs.affix', function() {

        if (!navbar.hasClass('affix')){

            navbar.addClass('animated slideInDown');

        }

    });


    navbar.on('affixed-top.bs.affix', function() {

        navbar.removeClass('animated slideInDown');

        

    });

    
    /*------- search form js -------*/

    $('.search_dropdown a').on('click', function(){

        if( $(this).parent().hasClass('open-search') ){

            $(this).parent().removeClass('open-search')

        }

        else{

            $(this).parent().addClass('open-search')

            $('.offcanvas_closer').addClass('show')

        }

        return false

    });

//navigation-header-js-Start


$(document).ready(function () {

                $(' .navbar-nav > li > .dropdown-menu > li').on('click', function () {

                    if ($(this).parent().parent().hasClass('open')) {

                        $(this).find(".dropdown-menu").toggleClass("opensubmenu");

                        if ($(this).children().hasClass("dropdown-menu")) {

//                            return false;

                        event.stopPropagation();

                        }

                    }

                });


                $(' .header-part .navbar-inverse .navbar-nav > li ').on('click', function () {

//                                 if($(this).hasClass('dropdown-toggle')){

                    $(".dropdown-menu").removeClass("opensubmenu");
//                                    }

                });


                if ($(window).width() < 991) {

                    $('.megamenu-content .title ').on('click', function () {

                        $(".megamenu-content .title").not($(this)).siblings().hide();

                        $(this).siblings().toggle();

//                        return false;

                       event.stopPropagation();

                    });

                }
               
            });

//navigation-header-js-End    

    

/* Main Slide Function*/

function sliderCarosule () {

    if ($('.slider_area .owl-carousel').length) {

        $('.slider_area .owl-carousel').owlCarousel({

            loop: true,

            nav: true,

            dots: false,

            autoplay: true,

            singleItem : true,

            animateIn: 'fadeIn',

              animateOut: 'fadeOut',

            navText: [

                '<i class="fa fa-angle-left"></i>',

                '<i class="fa fa-angle-right"></i>'

            ],

            smartSpeed: 1500,

            autoplayHoverPause: true,

            responsive: {

                0:{

                    items:1

                },

                480:{

                    items:1

                },

                600:{

                    items:1

                },

                1000:{

                    items:1

                },

                1200:{

                    items:1

                },

                1920:{

                    items:1

                }

            }

        });

    }

}

sliderCarosule ();



/* Service Slider Function*/

function serviceslidersecond () {

    if ($('.services .owl-carousel').length) {

        $('.services .owl-carousel').owlCarousel({

            loop: true,

            margin: 30,

            nav: false,

            dots: false ,

            autoplay: true,

            navText: [

                '<i class="fa fa-angle-left"></i>',

                '<i class="fa fa-angle-right"></i>'

            ],

            smartSpeed: 1000,

            autoplayHoverPause: true,

            responsive: {

                0:{

                    items:1

                },

                480:{

                    items:1

                },

                600:{

                    items:2

                },

                1000:{

                    items:4

                },

                1200:{

                    items:4

                },

                1920:{

                    items:4

                }

            }

        });

    }

}

serviceslidersecond ();  



/* After Before Gallery Function*/ 

function afterbeforeCarosule () {

    if ($('.after_before_gallery .owl-carousel').length) {

        $('.after_before_gallery .owl-carousel').owlCarousel({

            loop: true,

            margin: 30,

            nav: true,

            dots: false,

            autoplay: true,

            navText: [

                '<i class="fa fa-angle-left"></i>',

                '<i class="fa fa-angle-right"></i>'

            ],

            smartSpeed: 1500,

            autoplayHoverPause: true,

            responsive: {

                0:{

                    items:1

                },

                480:{

                    items:1

                },

                600:{

                    items:1

                },

                1000:{

                    items:1

                },

                1200:{

                    items:1

                },

                1920:{

                    items:1

                }

            }

        });

    }

}

afterbeforeCarosule ();


function equipment () {

    if ($('.equipment-slider.owl-carousel').length) {

        $('.equipment-slider.owl-carousel').owlCarousel({
            loop: true,
            items:1,
            margin:0,
            nav: true,
            dots: true,
            autoplay: true,
            navText: [

                '<i class="fa fa-angle-left"></i>',

                '<i class="fa fa-angle-right"></i>'

            ],

//            smartSpeed: 1500,

            autoplayHoverPause: true,

           responsive: {

                320:{

                    stagePadding:0,

                },

                490:{
                    stagePadding:100,

                },

                767:{
                stagePadding:100,

                },

                992:{
                    stagePadding:200,
                },

                
            },

         onTranslated:callBack

        });
        
        function callBack(){
          if ($(window).width() < 991) {
               $(".equipment-slider.owl-carousel .owl-item").css({height:"auto"});
            var owlstage= $(".equipment-slider.owl-carousel .owl-item.active").height();  
            console.log(owlstage);
            $(".equipment-slider .owl-item").css({height:owlstage}); 
            owlheight().null;
        }
        }

    }

}

equipment ();

/* equipment Function*/


function casestudy () {

    if ($('.casestudy-slider.owl-carousel').length) {

        $('.casestudy-slider.owl-carousel').owlCarousel({
            loop: false,
            items:1,
            margin:0,
            nav: true,
            dots: true,
            autoplay: false,
            navText: [

                '<i><img src="./img/case-study/case-next.png"></i>',

                '<i><img src="img/case-study/case-prev.png"></i>'

            ],

            autoplayHoverPause: true,
            responsive: {

                0:{

                    items:1

                },

                480:{

                    items:1

                },

                600:{

                    items:1

                },

                992:{

                   stagePadding:100,

                },
                

                
            },
            
            onTranslated:callBack

        });
        
        function callBack(){
          if ($(window).width() > 991) {
          if($('.casestudy-slider.owl-carousel .owl-item').last().hasClass('active')){
              $(".casestudy-slider .owl-stage").addClass("owlpadding-remove");
              $(".casestudy-slider").addClass("owlnav-pstn");
              var width = $(".casestudy-slider.owl-carousel .owl-item").width();
              $(".casestudy-slider.owl-carousel .owl-item:last-child").css({width:width + 100});
             }else {
                 $(".casestudy-slider .owl-stage").removeClass("owlpadding-remove");
                $(".casestudy-slider").removeClass("owlnav-pstn");
                 var currentwidth = $(".casestudy-slider.owl-carousel .owl-item").width();
                $(".casestudy-slider.owl-carousel .owl-item:last-child").css({width:currentwidth});
            }
        }
        }

    }

}

casestudy ();

/* casestudy Function*/


/* Testimonials Function*/

function testimonialsCarosuletwo () {

    if ($('.testimonials .owl-carousel').length) {

        $('.testimonials .owl-carousel').owlCarousel({

            loop: true,

            margin: 30,

            nav: true,

            dots: false ,

            autoplay: false,

            navText: [

                '<i class="fa fa-angle-left"></i>',

                '<i class="fa fa-angle-right"></i>'

            ],

            autoplayHoverPause: true,

            smartSpeed: 1500,

            responsive: {

                0:{

                    items:1

                },

                480:{

                    items:1

                },

                600:{

                    items:1

                },

                1000:{

                    items:1

                },

                1200:{

                    items:1

                },

                1920:{

                    items:1

                }

            }

        });

    }

}

testimonialsCarosuletwo ();  



/* Testimonials Function*/

function testimonials () {

    if ($('.testimonial-slider.owl-carousel').length) {

        $('.testimonial-slider.owl-carousel').owlCarousel({
            loop: true,
            nav: false,
            items:1,
            dots: true ,
             touchDrag  : false,
            mouseDrag  : false,
            arrowsnavigation : false,
            autoplay: false,
            autoplayHoverPause: true,
            animateIn: 'fadeIn', 
            animateOut: 'fadeOut' ,
            smartSpeed: 1500,
             responsive: {

                0:{

                    items:1

                },

                480:{

                    items:1

                },

                992:{

                    items:1

                }
                

            }
        });

    }

}

testimonials ();     



/* Team Function*/ 

function monialCarosule () {

    if ($('.testimonial-area .owl-carousel').length) {

        $('.testimonial-area .owl-carousel').owlCarousel({

            loop: true,

            margin: 30,

            nav: false,

            dots: true ,

            autoplay: true,

            navText: [

                '<i class="fa fa-angle-left"></i>',

                '<i class="fa fa-angle-right"></i>'

            ],

            autoplayHoverPause: true,

            responsive: {

                0:{

                    items:1

                },

                480:{

                    items:1

                },

                600:{

                    items:1

                },

                1000:{

                    items:2

                },

                1200:{

                    items:3

                },

                1920:{

                    items:3

                }

            }

        });

    }

}

monialCarosule ();

    

// add your custom functions 

    

/* Clients Logo Function*/

function clientCarosule () {

    if ($('#clients .owl-carousel').length) {

        $('#clients .owl-carousel').owlCarousel({

            loop: true,

            nav: true,

            dots: false,

            margin:70,

            autoWidth: true,

            navText: [

                '<i class="fa fa-angle-left"></i>',

                '<i class="fa fa-angle-right"></i>'

            ],

            autoplay: true,

            smartSpeed: 1500,

            autoplayTimeout: 3000,

            autoplayHoverPause: true,

            responsive: {

                0:{

                    items:1

                },

                480:{

                    items:2

                },

                600:{

                    items:3

                },

                1000:{

                    items:5

                },

                1200:{

                    items:5

                }

            }

        });

    }

}

clientCarosule();



/* Counter Function*/

function CounterNumberChanger () {

    var timer = $('.timer');

    if(timer.length) {

        timer.appear(function () {

            timer.countTo();

        })

    }



}

CounterNumberChanger();



/* Contact Form Function*/   

 function contactFormValidation () {

    if($('.contact_us_form').length){

        $('.contact_us_form').validate({ // initialize the plugin

            rules: {

                name: {

                    required: true

                },

                email: {

                    required: true,

                    email: true

                },

                message: {

                    required: true

                },

                subject: {

                    required: true

                }

            },

            submitHandler: function (form) { 

                // sending value with ajax request

                $.post($(form).attr('action'), $(form).serialize(), function (response) {

                    $(form).parent('div').append(response);

                    $(form).find('input[type="text"]').val('');

                    $(form).find('input[type="email"]').val('');

                    $(form).find('textarea').val('');

                });

                return false;

            }

        });

    }

}

contactFormValidation ();   



/* Video Popup Function*/    

    $(document).ready(function() {

        $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({

            disableOn: 700,

            type: 'iframe',

            mainClass: 'mfp-fade',

            removalDelay: 160,

            preloader: false,

            fixedContentPos: false

        });

    });

            

// scroll bottom to top button js Start

   

$(document).ready(function () {

    $(window).scroll(function () {

        if ($(this).scrollTop() > 150) {

                $('#scroll').fadeIn();

            } else {

                $('#scroll').fadeOut();

            }

        });

    $('#scroll').on('click', function () {

        $("html, body").animate({scrollTop: 0}, 600);

            return false;

    });

});



   

//  scroll bottom to top button js End

// === Count animations --start-- ===
    
    function Utils() {
    }
    Utils.prototype = {
        constructor: Utils,
        isElementInView: function (element, fullyInView) {
            if ($('.whychooseus-panel h3 strong i').hasClass('count')){
            var pageTop = $(window).scrollTop();
            var pageBottom = pageTop + $(window).height();
            
            var elementTop = $(element).offset().top;
            
            var elementBottom = elementTop + $(element).height();

            if (fullyInView === true) {
                return ((pageTop < elementTop) && (pageBottom > elementBottom));
            } else {
                return ((elementTop <= pageBottom) && (elementBottom >= pageTop));
            }
             }
        }
    };
    var Utils = new Utils();

    // ===**=== // 

    var count = 0;
    $(window).on('resize scroll', function () {
        var isElementInView = Utils.isElementInView($('.count'), true);
        if (isElementInView && !count) {
            $('.count').each(function () {
                $(this).prop('Counter', 0).animate({
                    Counter: $(this).text()
                }, {
                    duration: 3000,
                    easing: 'swing',
                    step: function (now) {
                        $(this).text(Math.ceil(now));
                    }
                });
            });
            count++;
        }
    });
    // === Count animations --end-- ===   

  
})(jQuery);


//  ABOUT-OUR-COMPANY-js-Start
$(document).ready(function () {
    $(".ourservice-panel").hover(function () {
        $(".ourservice-panel").not(this).removeClass("active");
        $(this).addClass("active");
    });
});
//  ABOUT-OUR-COMPANY-js-End



//  casestudy-js-Start
$(document).ready(function () {
    if ($(".casestudy-slider .owl-item:last-child").hasClass("active")){
         $(".casestudy-slider .owl-stage").addClass("faheem");
    }else {
        $(".casestudy-slider .owl-stage").removeClass("faheem");
    }
    
});
//  casestudy-js-End


//  equipment-slider-item-height-js-Start
$(document).ready(function () {
    if ($(window).width() < 991) {
        function owlheight() {
            var owlstage = $(".equipment-slider.owl-carousel .owl-item.active").height();
            $(".equipment-slider.owl-carousel .owl-item").css({height: owlstage});
        }
        owlheight();
    }

});
//  equipment-slider-item-height-js-End

            
//             .........WOW animation js Start.........
     jQuery(document).ready(function() {
              //===================
              //  WOW
              //  do not touch
              //===================
              new WOW().init();
            });
//             .........WOW animation js End.........
            