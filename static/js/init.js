(function($){
  $(function(){

    $('.sidenav').sidenav();
    $('.parallax').parallax();
    $('.carousel').carousel({
      fullWidth: true,
      indicators: true,
      duration: 500
    });
    
    setInterval(function () {
      $('.carousel').carousel('next');
      }, 5000);

  }); // end of document ready
})(jQuery); // end of jQuery name space

