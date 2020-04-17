//=====================================================================================

// 01.   Typed Text
// 02.   Navbar scrolling logo change
// 03.   Smoothscroll js
// 04.   Testimonial Slider
// 05.   Fact Counter For Achivement Counting
// 06.   Elements Animation
// 07.   When document is Scrollig
// 08.   LightBox / Fancybox
// 09.   Gallery With Filters List
// 10.   Youtube and Vimeo video popup control

//=====================================================================================

(function ($) {
  "use strict";

  var $body = $("body"),
    $window = $(window);

  $body.scrollspy({
    target: ".navbar-collapse",
    offset: 20,
  });

  /*=========================================================================== 
    // 00.   Navbar extra
    ============================================================================*/
  $("button.navbar-toggler").click(() => {
    let addClass = "nav-expanded";
    let navbar = $(".main_nav");
    if (navbar.hasClass(addClass)) navbar.removeClass(addClass);
    else navbar.addClass(addClass);
  });

  $(".blog_item").click(function () {
    var win = window.open($(this).attr("link"), "_blank");
    if (win) {
      //Browser has allowed it to be opened
      win.focus();
    } else {
      //Browser has blocked it
      alert("Please allow popups for this website.");
    }
  });
  $("body").click(() => {
    $(".navbar-collapse").collapse("hide");
  });

  /*=========================================================================== 
    // 01.   Typed Text
  ============================================================================*/

  $(".element").each(function () {
    var $this = $(this);
    $this.typed({
      strings: $this.attr("data-elements").split(","),
      typeSpeed: 100,
      backDelay: 3000,
    });
  });

  /*=========================================================================
  // 02.    Navbar scrolling logo change
  ===========================================================================*/

  $window.on("scroll", function () {
    var bodyScroll = $window.scrollTop(),
      navbar = $(".main_nav"),
      logo = $(".main_nav .navbar-brand> img");

    if (bodyScroll > 100) {
      navbar.addClass("nav-scroll");
    } else {
      navbar.removeClass("nav-scroll");
    }
  });

  /*=====================================================================   
  // 03.    Smoothscroll js
  =======================================================================*/

  $("a").on("click", function (event) {
    if (this.hash !== "") {
      event.preventDefault();

      var hash = this.hash;

      $("html, body").animate(
        {
          scrollTop: $(hash).offset().top,
        },
        1000,
        function () {
          window.location.hash = hash;
        }
      );
    }
  });

  //=====================================================================================
  //  04.   Testimonial Slider
  //=====================================================================================

  $(".testimonial_item").owlCarousel({
    loop: true,
    autoplay: true,
    autoplayTimeout: 5000,
    margin: 0,
    nav: true,
    dots: false,
    navText: [
      '<span class="fa fa-angle-left"></span>',
      '<span class="fa fa-angle-right"></span>',
    ],
    responsive: {
      0: {
        items: 1,
      },
      600: {
        items: 1,
      },
      1024: {
        items: 2,
      },
      1200: {
        items: 2,
      },
    },
  });

  //=====================================================================================
  // 05.    Fact Counter For Achivement Counting
  //=====================================================================================

  function iscountervisible($elementchecked) {
    var topview = $(window).scrollTop();
    var bottomview = topview + $(window).height();
    var topelement = $elementchecked.offset().top;
    var bottomelement = topelement + $elementchecked.height();
    return bottomelement <= bottomview && topelement >= topview;
  }

  function factCounter() {
    $(".fact-counter .count").each(function () {
      var $t = $(this);
      if (iscountervisible($t)) {
        var n = $t.find(".count-num").attr("data-stop"),
          r = parseInt($t.find(".count-num").attr("data-speed"), 10);

        if (!$t.hasClass("counted")) {
          $t.addClass("counted");
          $({
            countNum: $t.find(".count-num").text(),
          }).animate(
            {
              countNum: n,
            },
            {
              duration: r,
              easing: "linear",
              step: function () {
                $t.find(".count-num").text(Math.floor(this.countNum));
              },
              complete: function () {
                $t.find(".count-num").text(this.countNum);
              },
            }
          );
          //set skill building height
          var size = $t.children(".progress-bar").attr("aria-valuenow");
          $t.children(".progress-bar").css("width", size + "%");
        }
      }
    });
  }

  //=====================================================================================
  // 06.    Elements Animation
  //=====================================================================================

  if ($(".wow").length) {
    var wow = new WOW({
      boxClass: "wow", // animated element css class (default is wow)
      animateClass: "animated", // animation css class (default is animated)
      offset: 0, // distance to the element when triggering the animation (default is 0)
      mobile: false, // trigger animations on mobile devices (default is true)
      live: true, // act on asynchronously loaded content (default is true)
    });
    wow.init();
  }

  //=====================================================================================
  // 07.    When document is Scrollig
  //=====================================================================================

  $window.on("scroll touchmove", function () {
    factCounter();
  });
  //   $('body').bind('touchmove', function(e) {
  //     console.log("move");
  //     factCounter();
  // });

  //=====================================================================================
  //  08.   LightBox / Fancybox
  //=====================================================================================

  $('[data-fancybox="gallery"]').fancybox({
    animationEffect: "zoom-in-out",
    transitionEffect: "slide",
    transitionEffect: "slide",
  });

  //=====================================================================================
  //  09.   Gallery With Filters List
  //=====================================================================================

  if ($(".filter-list").length) {
    $(".filter-list").mixItUp({});
  }

  //=====================================================================================
  //  10.   Youtube and Vimeo video popup control
  //=====================================================================================

  jQuery(function () {
    jQuery("a.video-popup").YouTubePopUp();
    // jQuery("a.video-popup").YouTubePopUp( { autoplay: 1 } ); // Enable autoplay
  });
})(jQuery);

//=====================================================================================
//  11.   Backgroud crossfade
//=====================================================================================
var img_index = 1;
const N = 4;
const interval = 3000;

function cycleImages() {
  let img_name = "url('images/background/" + img_index.toString() + ".jpg')";
  $("#main_banner").css("background-image", img_name);
  $("#main_banner").css({
    "background-size": "cover",
    position: "relative",
  });

  img_index = (img_index + 1) % N;
}
function startCycle() {
  setInterval("cycleImages()", interval);
}
let loaded_count = 0;
Array.apply(null, { length: N })
  .map(Number.call, Number)
  .forEach((i) => {
    let img_path = "images/background/" + i.toString() + ".jpg";
    let downloadingImage = new Image();
    downloadingImage.onload = function () {
      loaded_count++;
      if (loaded_count == N) {
        startCycle();
      }
    };
    downloadingImage.src = img_path;
  });

//=====================================================================================
//  11.   MAIL
//=====================================================================================
// $("#send").click(function () {
//   let mail_subject = $("#mailSubject").val();
//   let mail_body = $("#mailMessage").val();
//   let mailApp = "mailto:contact@kenansoylu.com?subject=" + mail_subject + "&body=" + mail_body;
//   window.open(mailApp);
// });

$("#send").click(() => {
  alert("Mail temporarily disabled.");
  return;
  $("#mail-loading").css("display", "");

  const data = {
    sender_name: $("#mailName").val(),
    sender_mail: $("#senderMail").val(),
    mail_subject: $("#mailSubject").val(),
    mail_body: $("#mailMessage").val(),
  };

  $.ajax({
    type: "POST",
    url: "/send-mail",
    data: data,
    success: function (msg, status, jqXHR) {
      alert("Thanks for your message! I'll try to respond ASAP!");
      $("#mail-loading").css("display", "none");
    },
    error: function (jqXHR, textStatus, errorThrown) {
      alert("Couldn't send message... Sry :(");
      $("#mail-loading").css("display", "none");
    },
    dataType: "json",
  });
});

//=====================================================================================
//  12.   Carousel
//=====================================================================================
$(".carousel-control-prev").click(() => {
  $("#carouselExampleControls").carousel("prev");
});
$(".carousel-control-next").click(() => {
  $("#carouselExampleControls").carousel("next");
});

$("#carouselExampleControls").carousel({
  interval: 3000,
});
const PHOTO_RANGE = 24;
const PHOTO_COUNT_SECTION = 6;

let caro_items = [];

$(".carousel-img-container").each(function (carousel_item_index, _) {
  let photo_items = Array(PHOTO_COUNT_SECTION)
    .fill()
    .map((_, i) => {
      let img_index = carousel_item_index * PHOTO_COUNT_SECTION + i;
      if (img_index < PHOTO_RANGE) {
        let img_name =
          "images/portfolio/gallery/" + img_index.toString() + ".jpg";
        let a_href =
          "images/portfolio/gallery/" + img_index.toString() + ".jpg";

        let photo_item = $(".photo-item").clone();
        photo_item.attr("hidden", false);
        let downloadingImage = new Image();
        downloadingImage.onload = function () {
          $(".photo-item").eq(0).find("a").attr("data-fancybox", "");
          photo_item.find("a").attr("href", a_href);
          photo_item.find("img").attr("src", img_name);
        };
        downloadingImage.src = img_name;
        return photo_item;
      }
    });
  // $(".carousel-img-container").eq(carousel_item_index).append(photo_items);
  caro_items.push(photo_items);
});

$(".carousel-img-container").eq(0).append(caro_items[0]);
$(".carousel-img-container").eq(1).append(caro_items[1]);
$(".carousel-img-container").eq(2).append(caro_items[2]);
$(".carousel-img-container").eq(3).append(caro_items[3]);
$(".carousel-img-container").eq(4).append(caro_items[4]);
