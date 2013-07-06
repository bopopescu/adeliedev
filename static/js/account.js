$(document).ready(function() {
    $('.popbox').popbox({
       'open'          : '.open',
       'box'           : '.box',
       'arrow'         : '.arrow',
       'arrow_border'  : '.arrow_border',
       'close'         : '.close'
      });
})

$.ajaxSetup({
  data: {csrfmiddlewaretoken: csrftoken },
});

function login() {
    $(".regError").css("display", "none");
    username = $("#loginUser").val();
    pass = $("#loginPass").val();
    $.ajax({
        url: 'ajax/login',
        data: { 'username':username, 'pass':pass },
        type: "POST",
        success: function (response) {
                    if (response == "Success") {
                        location.reload()
                    }
                    else {
                        $("#loginError").css("display", "inline");
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
        url: 'ajax/checkuser/'+username,
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
            url: 'ajax/checkemail/'+email,
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
            url: 'ajax/reguser',
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
}

function showAccountEdit() {
    $("#accountInfo").css("display", "none");
    $("#editInfoForm").css("display", "inline");
}

function editAccount() {
    $(".error").css("display", "none");
    email = $("#email").val();
    currPass = $("#currPass").val();
    newPass = $("#newPass").val();
    confPass = $("#confPass").val();
    editGame = true;
    if (email == "") {
        $("#emailBlank").css("display", "inline");
        editGame = false;
    }
    else if (!isValidEmailAddress(email)) {
        $("#emailValid").css("display", "inline");
        editGame = false;
    }
    else {
        $.ajax({
            url: 'ajax/checkemail/'+email,
            async: false,
            success: function (response) {
                        if (response == "True") {
                            $("#emailTaken").css("display", "inline");
                            editGame = false;
                        }
                    }
        });
    }
    if (currPass == "") {
        $("#currPass").css("display", "inline");
        editGame = false;
    }
    else {
        $.ajax({
            url: 'ajax/checkpassword',
            data: {password:currPass},
            async: false,
            type: "POST",
            success: function (response) {
                        if (response == "True") {
                            $("#currPassWrong").css("display", "inline");
                            editGame = false;
                        }
                    }
        });
    }
    if (newPass == "" || newPass.length < 8) {
        $("#newPassValid").css("display", "inline");
        editGame = false;
    }
    if (confPass != newPass) {
        $("#confPassDifferent").css("display", "inline");
        editGame = false;
    }
    return editGame;
}