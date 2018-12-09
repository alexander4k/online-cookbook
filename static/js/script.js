$(document).ready(function() {
    // Materialize initializers
    $(".dropdown-trigger").dropdown();
    $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true
    });
    $('select').formSelect();
    $('.tooltipped').tooltip();
    $('.sidenav').sidenav();
    
    // Hide elements on page load
    $(".recent").hide();
    $(".oldest").hide();
    $(".sub_group.one").hide();
    $(".sub_group.two").hide();
    $(".sub_group.three").hide();
    
    // Change the favourite button icon/state/cursor
    changeFavouriteIconAndCursor(); 
    
    // Functionality of adding and removing ingredient and instruction fields
    addAndRemoveElements();
    
    // Functions for displaying carousels and their headings + arrows
    carouselArrows();
    carouselOptionsBehaviour(1);
    carouselOptionsBehaviour(2);
    carouselOptionsBehaviour(3);
    
    // Responsible for collapsing and expanding lists by clicking on their heading
    collapsibleLists(["#ingredients_expand",
        "#instructions_expand",
        "#allergens_expand",
        "#nutrition_expand"
    ]);
    
    // Pagination arrows either active or not depending on which page the user is on
    disableAndEnablePaginationArrows(".big");
    disableAndEnablePaginationArrows(".small");
    
    // Summary dropdowns behaviour
    show_and_hide_summary_groups();
    show_hide_mobile_summary_groups();
    switchArrowIconsForMobileSummary();
    
    // Printing the recipe details page
    printOnClick();
});

function changeFavouriteIconAndCursor() {
    /*
    Change the icon and cursor for favouriting recipes
    on hover and click 
    */
    $(".not_favourited").on({
        mousedown: function() {
            $(this).css("cursor", "pointer");
            $(this).removeClass("far").addClass("fas");
        },
        mouseup: function() {
            $(this).css("cursor", "pointer");
        },
        mouseover: function() {
            $(this).css("cursor", "pointer");
        },
    });
}

function removeClass(options_list) {
    /*
    Remove a class from a list of elements
    */
    var options = options_list;
    
    for (var i = 0; i < options.length; i++) {
        $(options[i]).removeClass("active");
    }
}

function showAndHideRestCarousel(show_option) {
    /*
    Apply the hide method to a list of elements and 
    a show method to a given element
    */
    var options_to_hide = [".popular", ".recent", ".oldest"];
    
    for (var i = 0; i < options_to_hide.length; i++) {
        $(options_to_hide[i]).hide();
    }
    
    $(show_option).show();
}

function carouselOptionsBehaviour(num_of_option) {
    /*
    Change the carousel headings and select to reflect which one is active. If a user
    on mobile selects a carousel to view e.g. recent, it will be reflected
    by the headings on bigger screens and vice versa.
    For an active carousel show it and hide the rest in.
    */
    
    // big screen set of heading options
    $(".carousel_option" + String(num_of_option)).click(function() {
        if (!$(this).hasClass("active")) {
            if (num_of_option == 1) {
                removeClass([".carousel_option2", ".carousel_option3"]);
                showAndHideRestCarousel(".popular");
                $("#carousel_options").val("1");
                $('select').formSelect();
            } else if (num_of_option == 2) {
                removeClass([".carousel_option1", ".carousel_option3"]);
                showAndHideRestCarousel(".recent");
                $("#carousel_options").val("2");
                $('select').formSelect();
            } else {
                removeClass([".carousel_option1", ".carousel_option2"]);
                showAndHideRestCarousel(".oldest");
                $("#carousel_options").val("3");
                $('select').formSelect();
            }
            
            $(this).addClass("active");
            $('.carousel.carousel-slider').carousel({
                fullWidth: true,
                indicators: true
            });
        }
    });
    
    // small screen select menu for options
    $("#carousel_options").change(function() {
        if ($(this).val() == 1) {
            removeClass([".carousel_option2", ".carousel_option3"]);
            showAndHideRestCarousel(".popular");
            $(".carousel_option1").addClass("active");
        } else if ($(this).val() == 2) {
            removeClass([".carousel_option1", ".carousel_option3"]);
            showAndHideRestCarousel(".recent");
            $(".carousel_option2").addClass("active");
        } else if ($(this).val() == 3) {
            removeClass([".carousel_option1", ".carousel_option2"]);
            showAndHideRestCarousel(".oldest");
            $(".carousel_option3").addClass("active");
        }
        
        $('.carousel.carousel-slider').carousel({
            fullWidth: true,
            indicators: true
        });
    });
}

function carouselArrows() {
    /*
    Gives the carousel arrows the functionality to move to the next 
    or previous slide
    */
    $('.moveNextCarousel').click(function(e) {
        e.preventDefault();
        e.stopPropagation();
        $('.carousel').carousel('next');
    });

    $('.movePrevCarousel').click(function(e) {
        e.preventDefault();
        e.stopPropagation();
        $('.carousel').carousel('prev');
    });
}

function addAndRemoveElements() {
    /*
    Create a new element inside a container when an add button is clicked
    and remove the last element inside the container when a remove button is clicked
    */
    $(".add_ingredient").click(function() {
        $(".ingredients").append('<div class="input-field col s12 m11 offset-m1 another"><textarea name="instruction" class="materialize-textarea"></textarea></div>');
    });

    $(".remove_ingredient").click(function() {
        $(".ingredients .another:last-child").last().remove();
    });

    $(".add_instruction").click(function() {
        $(".instructions").append('<div class="input-field col s12 m11 offset-m1 another"><textarea name="ingredient" class="materialize-textarea"></textarea></div>');
    });

    $(".remove_instruction").click(function() {
        $(".instructions .another:last-child").last().remove();
    });
}

function collapsibleLists(selectors) {
    /*
    Changes the icons on click and expands/collapses a list.
    For each selector, select its sibling and if the sibling is at 
    maximum height for that element, set the maxHeight to null otherwise
    set the maxHeight to the minimum height required for the element's content
    to fit in the viewport without using a vertical scrollbar
    */
    var list_of_selectors = selectors;
    
    for (var i = 0; i < list_of_selectors.length; i++) {
        $(list_of_selectors[i]).click(function() {
            if ($("#" + this.id + " i").hasClass("fa-caret-down")) {
                $("#" + this.id + " i").removeClass("fa-caret-down").addClass("fa-caret-up");
            } else if ($("#" + this.id + " i").hasClass("fa-caret-up")) {
                $("#" + this.id + " i").removeClass("fa-caret-up").addClass("fa-caret-down");
            }
            
            var list = this.nextElementSibling;

            if (list.style.maxHeight == 0 + "px") {
                list.style.maxHeight = list.scrollHeight + "px";
            } else {
                list.style.maxHeight = 0;
            }
        });
    }
}

function disableAndEnablePaginationArrows(pagination_class){
    /*
    Disable the previous and next arrow's pointer events and add/remove
    the disabled class to them depending on whether the current page is the 
    first or last 
    */
    if ($(pagination_class + " .num").first().hasClass("active")) {
        $(pagination_class + " .arrow").first().css('pointer-events', 'none');
        
        if (!$(pagination_class + " .arrow").first().hasClass("disabled")) {
            $(pagination_class + " .arrow").first().addClass("disabled");
        }
    } else {
        $(pagination_class + " .arrow").first().css('pointer-events', 'auto');
        
        if ($(pagination_class + " .arrow").first().hasClass("disabled")) {
            $(pagination_class + " .arrow").first().removeClass("disabled");
        }
    }
    
    if ($(pagination_class + " .num").last().hasClass("active")) {
        $(pagination_class + " .arrow").last().css('pointer-events', 'none');
        
        if (!$(pagination_class + " .arrow").last().hasClass("disabled")) {
            $(pagination_class + " .arrow").last().addClass("disabled");
        }
    } else {
        $(pagination_class + " .arrow").last().css('pointer-events', 'auto');
        
        if ($(pagination_class + " .arrow").last().hasClass("disabled")) {
            $(pagination_class + " .arrow").last().removeClass("disabled");
        }
    }
}

function show_and_hide_summary_groups(){
    /*
    Show and hide elements on hover
    */
    $(".group").mouseenter(function(){
        var list_of_classes = $(this).prop("classList");
        $(".sub_group." + list_of_classes[4]).show();
    });
    
    $(".group").mouseleave(function(){
        var list_of_classes = $(this).prop("classList");
        $(".sub_group." + list_of_classes[4]).hide();
    });
}

function show_hide_mobile_summary_groups(){
    /* 
    Show and hide an element on click
    */
    $(".mobile_group_heading").click(function(){
        var list_of_classes = $(this).prop("classList");
        $(".mobile_sub_group." + list_of_classes[1]).toggleClass("hidden");
    });
}

function switchArrowIconsForMobileSummary(){
    /*
    When a list is expanded by clicking on its heading, change the arrow
    to reflect that
    */
    $(".mobile_group_heading").click(function(){
        var list_of_classes = $(this).prop("classList");
        
        if ($(".mobile_group_heading." + list_of_classes[1] + " i").text() == "arrow_drop_down"){
            $(".mobile_group_heading." + list_of_classes[1] + " i").text("arrow_drop_up");
        } else {
            $(".mobile_group_heading." + list_of_classes[1] + " i").text("arrow_drop_down");
        }
    });
}

function printOnClick(){
    /*
    Fires when a print icon is clicked on the recipe_details page.
    Function to open a new window containing only the .general_details
    element's contents and apply a separate stylesheet to it. Opens
    a print window after .7s(to allow the styles to kick in) and once printed
    closes the window.
    */
    $(".print").click(function() {
        var w=window.open();
        w.document.write($(".details").html());
        w.document.write('<link rel="stylesheet" type="text/css" href="/static/css/print_style.css">');
        setTimeout(function(){
            w.print();
            w.close();
        }, 700);
    });
}

