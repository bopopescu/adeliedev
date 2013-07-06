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
        url: '/ajax/login',
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

toggle = true;
function toggleBillingAddress() {
    if (toggle) {
        $("#billingForm").css("display", "inline");
        toggle = false;
    }
    else {
        $("#billingForm").css("display", "none");
        toggle = true;
    }
}

function placeYourOrder() {
	$(".error").css("display", "none");
    shippingName = $("#shippingName").val();
    shippingAddressOne = $("#shippingAddressOne").val();
    shippingAddressTwo = $("#shippingAddressTwo").val();
    shippingCity = $("#shippingCity").val();
    shippingState = $("#shippingState").val();
    shippingZip = $("#shippingZip").val();
	sameAsShipping = $("#sameAsShipping").is(':checked');
    billingName = $("#billingName").val();
    billingAddressOne = $("#billingAddressOne").val();
    billingAddressTwo = $("#billingAddressTwo").val();
    billingCity = $("#billingCity").val();
    billingState = $("#billingState").val();
    billingZip = $("#billingZip").val();
    paymentName = $("#paymentName").val();
    paymentCard = $("#paymentCard").val();
    paymentMonth = $("#paymentMonth").val();
    paymentYear = $("#paymentYear").val();
    paymentCode = $("#paymentCode").val();
	placeOrder = true;
	var zipPattern = new RegExp(/^\d{5}(-\d{4})?$/);
	if (shippingName == "") {
		$("#errorShippingName").css("display", "inline");
		placeOrder = false;
	}
	if (shippingAddressOne == "") {
		$("#errorShippingAddress").css("display", "inline");
		placeOrder = false;
	}
	if (shippingCity == "") {
		$("#errorShippingCity").css("display", "inline");
		placeOrder = false;
	}
	if (shippingState == "") {
		$("#errorShippingState").css("display", "inline");
		placeOrder = false;
	}
	if (shippingZip == "" || !zipPattern.test(shippingZip)) {
		$("#errorShippingZip").css("display", "inline");
		placeOrder = false;
	}
	if (billingName == "" && !sameAsShipping) {
		$("#errorBillingName").css("display", "inline");
		placeOrder = false;
	}
	if (billingAddressOne == "" && !sameAsShipping) {
		$("#errorBillingAddress").css("display", "inline");
		placeOrder = false;
	}
	if (billingCity == "" && !sameAsShipping) {
		$("#errorBillingCity").css("display", "inline");
		placeOrder = false;
	}
	if (billingState == "" && !sameAsShipping) {
		$("#errorBillingState").css("display", "inline");
		placeOrder = false;
	}
	if ((billingZip == "" || !zipPattern.test(billingZip)) && !sameAsShipping) {
		$("#errorBillingZip").css("display", "inline");
		placeOrder = false;
	}
	if (paymentName == "") {
		$("#errorPaymentName").css("display", "inline");
		placeOrder = false;
	}
	var visaPattern = new RegExp(/^4[0-9]{12}(?:[0-9]{3})?$/);
	var masterCardPattern = new RegExp(/^5[1-5][0-9]{14}$/);
	var amexPattern = new RegExp(/^3[47][0-9]{13}$/);
	var dinersPattern = new RegExp(/^3(?:0[0-5]|[68][0-9])[0-9]{11}$/);
	var discoverPattern = new RegExp(/^6(?:011|5[0-9]{2})[0-9]{12}$/);
	var jcbPattern = new RegExp(/^(?:2131|1800|35\d{3})\d{11}$/);
	cardType = "none";
	if (paymentCard == "") {
		$("#errorPaymentCard").css("display", "inline");
		placeOrder = false;
	}
	else {
		paymentCard.replace(/[^0-9]+/, "");
		if (visaPattern.test(paymentCard))
			cardType = "visa";
		else if (masterCardPattern.test(paymentCard))
			cardType = "master card";
		else if (amexPattern.test(paymentCard))
			cardType = "american express";
		else if (dinersPattern.test(paymentCard))
			cardType = "diner's club";
		else if (discoverPattern.test(paymentCard))
			cardType = "discover";
		else if (jcbPattern.test(paymentCard))
			cardType = "jcb";
		if (cardType == "none") {
			$("#errorPaymentCard").css("display", "inline");
			placeOrder = false;
		}
	}
	if (paymentMonth == "" || paymentYear == "") {
		$("#errorPaymentDate").css("display", "inline");
		placeOrder = false;
	}
	if (paymentCode == "") {
		$("#errorPaymentCode").css("display", "inline");
		placeOrder = false;
	}
	return placeOrder;
}