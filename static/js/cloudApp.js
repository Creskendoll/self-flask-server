jQuery(document).ready(function($){
    const leftArrow = "https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-arrow-left-b-512.png";
    const downArrow = "https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-arrow-down-b-512.png";

    $(".question-container").click(function() {
        let arrowImg = $(this).find(".expand-arrow-image");
        const current = arrowImg.attr("src");
        arrowImg.attr("src", current === leftArrow ? downArrow : leftArrow);
    });
});