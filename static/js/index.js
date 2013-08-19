active = 1;
$(document).ready(function() {
    $.each(all_products, function(index, value) {
        $("#countdown_game_" + value[0]).countdown({until: value[1]});
    });
    if (upcoming_countdown) {
        $("#countdown_upcoming").countdown({until: upcoming_countdown});
    }
});
function changeSlide(slideId) {
    if (slideId > active) {
        $(".slide").hide("slide", {direction: "left"}, 1000);
        $("#slide" + slideId).show("slide", {direction: "right"}, 1000);
    }
    else if (slideId < active) {
        $(".slide").hide("slide", {direction: "right"}, 1000);
        $("#slide" + slideId).show("slide", {direction: "left"}, 1000);
    }
    active = slideId;
}
function change_picture(product_id, picture_url) {
    $('#main_picture_product_' + product_id).attr("src", picture_url);
}
