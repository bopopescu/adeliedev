$(function() {
    $('#product_start').datepicker();
    $('#product_end').datepicker();
    $('#product_ship').datepicker();
    $('#product_start_time').timepicker({ 'timeFormat': 'H:i:s' });
    $('#product_end_time').timepicker({ 'timeFormat': 'H:i:s' });
});

function submitGame() {
    $(".error").css("display", "none");
    name = $("#product_name").val();
    description = $("#product_desc").val();
    start = $("#product_start").val();
    startTime = $("#product_start_time").val();
    end = $("#product_end").val();
    endTime = $("#product_end_time").val();
    ship = $("#product_ship").val();
    price = $("#product_price").val();
    tagline = $("#product_tag_line").val();
    saveGame = true;
    if (name == "") {
        $("#titleBlank").css("display", "inline");
        saveGame = false;
    }
    else {
        $.ajax({
            url: '/ajax/checkproductname/' + name,
            async: false,
            success: function (response) {
                        if (response == "True") {
                            $("#titleDuplicate").css("display", "inline");
                            saveGame = false;
                        }
                    }
        });
    }
    if (tagline == "") {
        $("#tagBlank").css("display", "inline");
        saveGame = false;
    }
    if (price == "") {
        $("#priceBlank").css("display", "inline");
        saveGame = false;
    }
    if (price < 0) {
        $("#priceBelowZero").css("display", "inline");
        saveGame = false;
    }
    if (description == "") {
        $("#descBlank").css("display", "inline");
        saveGame = false;
    }
    if (start == "" || startTime == "") {
        $("#startBlank").css("display", "inline");
        saveGame = false;
    }
    if (end == "" || endTime == "") {
        $("#endBlank").css("display", "inline");
        saveGame = false;
    }
    if (end < start) {
        $("#timeDiff").css("display", "inline");
        saveGame = false;
    }
    if (ship == "") {
        $("#shipBlank").css("display", "inline");
        saveGame = false;
    }
    if (ship < end) {
        $("#shipError").css("display", "inline");
        saveGame = false;
    }

    if (saveGame) {
        $.ajax({
            url: '/ajax/saveproduct',
            data: {name: name, desc: description, start: start, startTime: startTime, end: end, endTime: endTime, price: price, ship:ship, tagline:tagline},
            type: "POST",
            async: false,
            success: function (response) {
                        if (response == "False") {
                            $("#unknownErorr").css("display", "inline");
                            regGame = false;
                        }
                        else if (typeof parseInt(response) == "number") {
                            window.location = "/admin/showproduct/" + response;
                        }
                    }
        });
    }
}

function giveCredit(gameId) {
    $.ajax({
        url: '/ajax/givecredit',
        data: {gameId:gameId},
        type: "POST",
        async: false,
        success: function (response) {
                    //window.location = "/admin/showcredit/" + gameId;
                }
    });
}
