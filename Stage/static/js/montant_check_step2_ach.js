
 $(document).ready(function(){
    $('#step2').on("click", function(e) {
      e.preventDefault();
        var total = 0;
        $('.qu').each(function(ind) {
            var prix = $('.na').eq(ind).val();
            var quantite = $(this).val();
            if(!prix || !quantite){
               md.showNotificationDelete('top','center','danger','check your empty inputs !');

            }
            prix = (isNaN(prix) || (prix == '') )?0:parseInt(prix);
            quantite = (isNaN(quantite) || (quantite == ''))?0:parseInt(quantite);
            total += prix * quantite;
        });
        var sah = Cookies.get('montant')
        if (total > sah){
          var message = 'Le Total des articles ne correspond pas à le montant HT   : ' + total
          md.showNotificationDelete('top','center','danger',message);
            $('#done').addClass('disabled');
          }
          else{
                      $('#done').removeClass('disabled');

          }
    });

    });