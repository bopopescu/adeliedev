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
        $("#errorShippingName").css("display", "block");
        placeOrder = false;
    }
    if (shippingAddressOne == "") {
        $("#errorShippingAddress").css("display", "block");
        placeOrder = false;
    }
    if (shippingCity == "") {
        $("#errorShippingCity").css("display", "block");
        placeOrder = false;
    }
    if (shippingState == "") {
        $("#errorShippingState").css("display", "block");
        placeOrder = false;
    }
    if (shippingZip == "" || !zipPattern.test(shippingZip)) {
        $("#errorShippingZip").css("display", "block");
        placeOrder = false;
    }
    if (billingName == "" && !sameAsShipping) {
        $("#errorBillingName").css("display", "block");
        placeOrder = false;
    }
    if (billingAddressOne == "" && !sameAsShipping) {
        $("#errorBillingAddress").css("display", "block");
        placeOrder = false;
    }
    if (billingCity == "" && !sameAsShipping) {
        $("#errorBillingCity").css("display", "block");
        placeOrder = false;
    }
    if (billingState == "" && !sameAsShipping) {
        $("#errorBillingState").css("display", "block");
        placeOrder = false;
    }
    if ((billingZip == "" || !zipPattern.test(billingZip)) && !sameAsShipping) {
        $("#errorBillingZip").css("display", "block");
        placeOrder = false;
    }
    if (paymentName == "") {
        $("#errorPaymentName").css("display", "block");
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
        $("#errorPaymentCard").css("display", "block");
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
            $("#errorPaymentCard").css("display", "block");
            placeOrder = false;
        }
    }
    if (paymentMonth == "" || paymentYear == "") {
        $("#errorPaymentDate").css("display", "block");
        placeOrder = false;
    }
    if (paymentCode == "") {
        $("#errorPaymentCode").css("display", "block");
        placeOrder = false;
    }
    return placeOrder;
}
