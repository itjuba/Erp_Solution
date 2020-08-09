
 $(document).ready(function(){
    $('#step2').on("click", function(e) {
      e.preventDefault();
      var total = 0;
      $('.qu').each(function(ind) {
          var prix = $('.na').eq(ind).val();
          console.log(prix);
          var quantite = $(this).val();
          console.log(quantite);
          if(!prix || !quantite){
             md.showNotificationDelete('top','center','danger','check your empty inputs !');

          }
          prix = (isNaN(prix) || (prix == '') )?0:parseFloat(prix);
          quantite = (isNaN(quantite) || (quantite == ''))?0:parseInt(quantite);
          total += (prix * quantite);
          console.log(total);
      });
      var sah = Cookies.get('montant')
      console.log(sah)
      console.log(total)
      if (total != sah){
        var message = 'Le Total des articles ne correspond pas à le montant HT   :  total =' + ' ' + total + ' ' + 'Montant HT = ' + sah
        md.showNotificationDelete('top','center','danger',message);
        $('#done').attr('disabled','disabled');
        }
        else{
                    $('#done').removeAttr('disabled');


        }
    });

    });