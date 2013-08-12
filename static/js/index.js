active = 1;
function changeSlide(slideId) {
    if (slideId > active) {
        $(".slide").hide("slide", {direction: "left"}, 1000);
        $("#slide" + slideId).show("slide", {direction: "right"}, 1000);
    }
    else if (slideId < active) {
        $(".slide").hide("slide", {direction: "right"}, 1000);
        $("#slide" + slideId).show("slide", {direction: "left"}, 1000);
    }
    active = slideId;
}
