function updateQuantity(itemId) {
    quantity = $("#" + itemId + "_quantity").val()
    $.ajax({
        url: '/ajax/updatecart',
        data: { 'itemId': itemId, 'quantity': quantity },
        type: "POST",
        async: false,
        success: function (response) {
                    location.reload()
                }
    });
}

function deleteItem(itemId) {
    $("#" + itemId + "_quantity").val(0);
    updateQuantity(itemId);
}
