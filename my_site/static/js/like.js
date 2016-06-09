$(document).ready(function(){
    $('#like_button_country').click(function(){
        id = $(this).attr("data");
        $.ajax({
               url: '/update_like_country2/',
               method: 'POST',
               dataType: 'json',
               data: {"id": id}
         }).done(function(data) {
            if (data.is_liked) {
                $('#not_liked_img').css("display", "none");
                $('#liked_img').css("display", "inline");
                $('#likes_count_text').text(data.likes_count);
            } else {
                $('#liked_img').css("display", "none");
                $('#not_liked_img').css("display", "inline");
                $('#likes_count_text').text(data.likes_count);
            }
         })
    })

    $('#like_button_city').click(function(){
        id = $(this).attr("data");
        $.ajax({
               url: '/update_like_city2/',
               method: 'POST',
               dataType: 'json',
               data: {"id": id}
         }).done(function(data) {
            if (data.is_liked) {
                $('#not_liked_img').css("display", "none");
                $('#liked_img').css("display", "inline");
                $('#likes_count_text').text(data.likes_count);
            } else {
                $('#liked_img').css("display", "none");
                $('#not_liked_img').css("display", "inline");
                $('#likes_count_text').text(data.likes_count);
            }
         })
    })

    $('#like_button_person').click(function(){
        id = $(this).attr("data");
        $.ajax({
               url: '/update_like_person2/',
               method: 'POST',
               dataType: 'json',
               data: {"id": id}
         }).done(function(data) {
            if (data.is_liked) {
                $('#not_liked_img').css("display", "none");
                $('#liked_img').css("display", "inline");
                $('#likes_count_text').text(data.likes_count);
            } else {
                $('#liked_img').css("display", "none");
                $('#not_liked_img').css("display", "inline");
                $('#likes_count_text').text(data.likes_count);
            }
         })
    })
});
