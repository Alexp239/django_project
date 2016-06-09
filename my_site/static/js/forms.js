$(document).ready(function(){
    $("#tag").autocomplete({
      source: "/autocomplete_tags/",
      minLength: 2
    });
});
