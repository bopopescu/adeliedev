$(function() {
    $('#product_start').datepicker();
    $('#product_end').datepicker();
    $('#product_ship').datepicker();
    $('#product_start_time').timepicker({ 'timeFormat': 'H:i:s' });
    $('#product_end_time').timepicker({ 'timeFormat': 'H:i:s' });
});

function editGame() {
    $(".error").css("display", "none");
    name = $("#product_name").val();
    description = $("#product_desc").val();
    start = $("#product_start").val();
    start_time = $("#product_start_time").val();
    end = $("#product_end").val();
    end_time = $("#product_end_time").val();
    price = $("#product_price").val();
    product_id = $("#product_id").val();
    tagline = $("#product_tag_line").val();
    ship = $("#product_ship").val();
    edit_game = true;
    if (name == "") {
        $("#titleBlank").css("display", "inline");
        edit_game = false;
    }
    if (tagline == "") {
        $("#tagBlank").css("display", "inline");
        edit_game = false;
    }
    if (description == "") {
        $("#descBlank").css("display", "inline");
        edit_game = false;
    }
    if (price == "") {
        $("#priceBlank").css("display", "inline");
        edit_game = false;
    }
    if (price < 0) {
        $("#priceBelowZero").css("display", "inline");
        edit_game = false;
    }
    if (start == "" || start_time == "") {
        $("#startBlank").css("display", "inline");
        edit_game = false;
    }
    if (end == "" || end_time == "") {
        $("#endBlank").css("display", "inline");
        edit_game = false;
    }
    if (end < start) {
        $("#timeDiff").css("display", "inline");
        edit_game = false;
    }
    if (ship == "") {
        $("#shipBlank").css("display", "inline");
        edit_game = false;
    }
    if (ship < end) {
        $("#shipError").css("display", "inline");
        edit_game = false;
    }
    if (typeof parseInt(product_id) != "number") {
        edit_game = false;
    }

    if (edit_game) {
        $.ajax({
            url: '/ajax/editproduct',
            data: {name: name, desc: description, start: start, start_time:start_time, end: end, end_time:end_time, product_id: product_id, price: price, ship:ship, tagline:tagline},
            type: "POST",
            async: false,
            success: function (response) {
                        if (response == "False") {
                            $("#unknownErorr").css("display", "inline");
                        }
                        else if (typeof parseInt(response) == "number") {
                            window.location = "/admin/showproduct/" + response;
                        }
                    }
        });
    }
}

function deletePic(picId) {
    $.ajax({
        url: '/ajax/deletepic',
        data: {picId: picId},
        type: "POST",
        async: false,
        success: function (response) {
                    location.reload();
                }
    });
}
