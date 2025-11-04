/* Placeholder gallery script to prevent 404s. Add gallery-specific code here if needed. */
(function(){
  if (typeof window !== 'undefined') {
    // no-op; reserved for gallery interactions
  }
})();


    $(document).ready(function () {
      $('.client-logo').owlCarousel({
        loop: true,
        margin: 0,
        dots: false,
        nav: false,
        autoplay: true,
        autoplayTimeout: 1500,
        autoplayHoverPause: false,
        responsive: {
          0: { items: 3 },
          600: { items: 4 },
          1000: { items: 6 }
        }
      });
    });
