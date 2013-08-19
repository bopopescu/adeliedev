$(document).ready(function() {
    $.each(upcoming_products, function(index, value) {
        $("#countdown_game_" + value[0]).countdown({until: value[1]});
    });
});
