 $(document).ready(function() {

      $('.search').click(function(){
 var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
 var el= this;
 const artists_div = $('#replaceable-content')
     var title = $('.da option:selected').val();
      var price = $('.price').val();
       var date = $('.date').val();
       console.log(title)
       console.log(price)
       console.log(date)

      $.ajax({
               type: "POST",
               url: '/search/ajax/',
               data: JSON.stringify({'title' : title,'price':price,'date':date}),
                headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-CSRFToken": csrftoken
            },

               success: function(response) {
                    artists_div.fadeTo('slow', 0).promise().then(() => {
                // replace the HTML contents
                artists_div.html(response['html_from_view'])
                // fade-in the div with new contents
                artists_div.fadeTo('slow', 1)

                if (response['html_from_view']==''){
                console.log('not found ! ')}
            })

                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          });
    })
    });