$(document).ready(function() {
    $('.popbox').popbox({
       'open'          : '.open',
       'box'           : '.box',
       'arrow'         : '.arrow',
       'arrow_border'  : '.arrow_border',
       'close'         : '.close'
      });

})

$(function() {
    $('#gameStart').datepicker();
    $('#gameEnd').datepicker();
});

$.ajaxSetup({
  data: {csrfmiddlewaretoken: csrftoken },
});

function login(num) {
    $(".regError").css("display", "none");
    username = $("#loginUser" + num).val();
    pass = $("#loginPass" + num).val();
    $.ajax({
        url: '/ajax/login',
        data: { 'username':username, 'pass':pass },
        type: "POST",
        success: function (response) {
                    if (response == "Success") {
                        location.reload()
                    }
                    else {
                        $("#loginError" + num).css("display", "inline");
                    }
                }
    });
}

function register() {
    $(".regError").css("display", "none");
    username = $("#username").val();
    email = $("#email").val();
    pass1 = $("#pass1").val();
    pass2 = $("#pass2").val();
    regUser = true;
    if (username == "") {
        $("#blankUserError").css("display", "inline");
        regUser = false;
    }
    if (email == "") {
        $("#blankEmailError").css("display", "inline");
        regUser = false;
    }
    if (email != "" && !isValidEmailAddress(email)) {
        $("#validEmailError").css("display", "inline");
        regUser = false;
    }
    if (pass1 == "") {
        $("#blankPassError").css("display", "inline");
        regUser = false;
    }
    if (pass1 != "" && pass1 != pass2) {
        $("#passError").css("display", "inline");
        regUser = false;
    }
    $.ajax({
        url: '/ajax/checkuser/'+username,
        async: false,
        success: function (response) {
                    if (response == "True") {
                        $("#userError").css("display", "inline");
                        regUser = false;
                    }
                    else {
                        regUser = true && regUser;
                    }
                }
    });
    if (regUser) {
        $.ajax({
            url: '/ajax/checkemail/'+email,
            async: false,
            success: function (response) {
                        if (response == "True") {
                            $("#emailError").css("display", "inline");
                            regUser = false;
                        }
                        else {
                            regUser = true && regUser;
                        }
                    }
        });
    }
    if (regUser) {
        $.ajax({
            url: '/ajax/reguser',
            data: { 'email':email, 'username':username, 'pass1': pass1, 'pass2':pass2 },
            type: "POST",
            async: false,
            success: function (response) {
                        if (response == "Success") {
                            $("#regForm").css("display", "none");
                            $("#regSuccess").css("display", "inline");
                        }
                        else {
                            alert("We are sorry there was an error registering your account. Please refresh and try again");
                        }
                    }
        });
    }
}

function isValidEmailAddress(emailAddress) {
    var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
    return pattern.test(emailAddress);
};

function editGame() {
    $(".error").css("display", "none");
    title = $("#gameTitle").val();
    publisher = $("#gamePublisher").val();
    description = $("#gameDesc").val();
    start = $("#gameStart").val();
    end = $("#gameEnd").val();
    price = $("#gamePrice").val();
    gameId = $("#gameId").val();
    tagline = $("#gameTagline").val();
    ship = $("#gameShip").val();
    consoles = $("#gameConsoles").val();
    editGame = true;
    if (title == "") {
        $("#titleBlank").css("display", "inline");
        editGame = false;
    }
    if (tagline == "") {
        $("#tagBlank").css("display", "inline");
        editGame = false;
    }
    if (publisher == "") {
        $("#publisherBlank").css("display", "inline");
        editGame = false;
    }
    if (description == "") {
        $("#descBlank").css("display", "inline");
        editGame = false;
    }
    if (price == "") {
        $("#priceBlank").css("display", "inline");
        editGame = false;
    }
    if (price < 0) {
        $("#priceBelowZero").css("display", "inline");
        editGame = false;
    }
    if (start == "") {
        $("#startBlank").css("display", "inline");
        editGame = false;
    }
    if (end == "") {
        $("#endBlank").css("display", "inline");
        editGame = false;
    }
    if (end < start) {
        $("#timeDiff").css("display", "inline");
        editGame = false;
    }
    if (ship == "") {
        $("#shipBlank").css("display", "inline");
        saveGame = false;
    }
    if (ship < end) {
        $("#shipError").css("display", "inline");
        saveGame = false;
    }
    if (consoles == null) {
        $("#consoleBlank").css("display", "inline");
        saveGame = false;
    }
    if (typeof parseInt(gameId) != "number") {
        editGame = false;
    }
    
    if (editGame) {
        $.ajax({
            url: '/ajax/editgame',
            data: {title: title, publisher: publisher, desc: description, start: start, end: end, gameid: gameId, price: price, ship:ship, consoles:consoles, tagline:tagline},
            type: "POST",
            async: false,
            success: function (response) {
                        if (response == "False") {
                            $("#unknownErorr").css("display", "inline");
                        }
                        else if (typeof parseInt(response) == "number") {
                            window.location = "/admin/showgame/" + response;
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

function deleteVideo(videoId) {
    $.ajax({
        url: '/ajax/deletevideo',
        data: {videoId: videoId},
        type: "POST",
        async: false,
        success: function (response) {
                    location.reload();
                }
    });
}

function s3_upload(){
    var s3upload = new S3Upload({
        file_dom_selector: '#id_video',
        s3_sign_put_url: '/sign_s3_upload',

        onProgress: function(percent, message) { 
            $('#status').html('Upload progress: ' + percent + '%' + message);
        },
        onFinishS3Put: function(url) { 
            $('#status').html('');
            gameId = $("#gameId").val()
            $.ajax({
                url: '/ajax/addtrailer',
                data: {url: url, gameId:gameId},
                type: "POST",
                async: false,
                success: function (response) {
                            location.reload();
                        }
            });
        },
        onError: function(status) {
            $('#status').html('Upload error: ' + status);
        }
    });
}