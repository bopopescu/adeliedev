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
