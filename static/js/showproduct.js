$(document).ready(function () {
    $("#countdown").countdown({until: product_countdown});
});

function add_to_cart(product_id) {
    quantity = $("#orderQuantity").val();
    $.ajax({
        url: '/ajax/addtocart',
        data: { 'product_id':product_id, 'quantity':quantity },
        type: "POST",
        async: false,
        success: function (response) {
                    window.location = "/cart";
                }
    });
}
