
 $(document).ready(function(){
         $('.nadjib').on("click",function(){
    if($('#sidebar').hasClass('attig')){
    console.log('yes');
        $('#sidebar').animate({
               left: '-300px'
            }, 600);
            $('#sidebar').removeClass('attig')
            $('.main-panel').animate({
                left: '-275px',

            }, 600);
                 $('#content').animate({
                   width:'1250px',


            }, 600);




    }


  else{
     $('#sidebar').animate({
                left: '0px'
            }, 600);
              $('#sidebar').addClass('attig')
                $('#content').removeClass('cardd');
            $('.main-panel').animate({
                left: '1px',

            }, 600);
                   $('#content').animate({
                   width:'1150px',


            }, 600);
  }


  });
    });