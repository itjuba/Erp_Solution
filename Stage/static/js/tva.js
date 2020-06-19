
$(document).ready(function(){
   //Jquery Code

   $(document).on('keyup',"[name='tv']",function(){
        console.log('in');
        var tva= $("[name='tv']").val()
        var ht= $('input[name=Montant_HT]').val()
        console.log(tva)
        var total = (tva * $("[name='Montant_HT']").val())/100;

        $("input[name=Montant_TVA]").val(total);
        $('#label1').addClass('is-focused');
        console.log(total);
        t = Number(total) + Number(ht);
        console.log(t);



        $('input[name=Montant_TTC]').val(t);
         $('#label').addClass('is-focused');



        });

         $(document).on('keyup',"[name='Montant_HT']",function(){
        console.log('in');
        var tva= $("[name='tv']").val()
        var ht= $('input[name=Montant_HT]').val()
        console.log(tva)
        var total = (tva * $("[name='Montant_HT']").val())/100;

        $("input[name=Montant_TVA]").val(total);
        $('#label1').addClass('is-focused');
        console.log(total);
        t = Number(total) + Number(ht);
        console.log(t);



        $('input[name=Montant_TTC]').val(t);
         $('#label').addClass('is-focused');



        });
});
