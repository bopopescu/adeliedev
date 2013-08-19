$(document).ready(function() {
    $.each(product_countdowns, function(index, value) {
        $("#countdown_game_" + value[0]).countdown({until: value[1]});
    });
});

function sortByName(a, b) {
    var aName = a['title'].toLowerCase();
    var bName = b['title'].toLowerCase();
    return ((aName < bName) ? -1 : ((aName > bName) ? 1 : 0));
}

function sortByEnding(a, b) {
    var aEnd = a['end'];
    var bEnd = b['end'];
    return ((aEnd < bEnd) ? -1 : ((aEnd > bEnd) ? 1 : 0));
}

function sortByLeastBought(a, b) {
    var aBought = a['purchased'];
    var bBought = b['purchased'];
    return ((aBought < bBought) ? -1 : ((aBought > bBought) ? 1 : 0));
}

function sortByMostBought(a, b) {
    var aBought = a['purchased'];
    var bBought = b['purchased'];
    return ((aBought > bBought) ? -1 : ((aBought < bBought) ? 1 : 0));
}

function sort_products() {
    sort = $("#sort").val();
    if (sort == "alphabetical") {
        products.sort(sortByName);
    }
    else if (sort == "ending") {
        products.sort(sortByEnding);
    }
    else if (sort == "most") {
        products.sort(sortByMostBought);
    }
    else if (sort == "least") {
        products.sort(sortByLeastBought);
    }
    products_list= ""
    $.each(products, function (index, value) {
        products_list+= "<li id='list" + value['id'] + "'>" + $("#list" + value['id']).html() + "</div>";
    });
    $("#products_list li").remove();
    $("#products_list").append(products_list);
}
