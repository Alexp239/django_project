$(document).ready(function(){
    $('#like_button').click(function(){
        id = $(this).attr("country_id");
        is_like = $(this).attr("is_like");
        $.ajax({
               url: UpdateLikeCountry,
               method: 'POST',
               dataType: 'json',
               data: {"object_id": country_id,
                    "is_like": is_like}
         }).done(function(data)) {

         }
    })
});
