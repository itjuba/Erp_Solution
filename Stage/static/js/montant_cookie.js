
 $(document).ready(function(){
   $('#step1').on("click", function(e) {
      var mont = $('.mont').val()
      Cookies.set('montant',mont);

    });

    });