$(document).ready(function() {
    $(".recent").hide()
    $(".oldest").hide()
    $(".favourites").hide()
    $('.sidenav').sidenav();
    $('.tooltipped').tooltip();
    refreshSlide()
    refreshSelect()
    changeFavouriteIconAndCursor()
    addAndRemoveElements()
    carouselArrows()
    carouselOptionsBehaviour(1)
    carouselOptionsBehaviour(2)
    carouselOptionsBehaviour(3)
    profileOptionsBehaviour(1)
    profileOptionsBehaviour(2)
    collapsibleLists(["#ingredients_expand",
        "#instructions_expand",
        "#allergens_expand",
        "#nutrition_expand"
    ])
    disableAndEnablePaginationArrows(".big")
    disableAndEnablePaginationArrows(".small")
});

function changeFavouriteIconAndCursor() {
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

function refreshSelect() {
    $('select').formSelect();
}

function refreshSlide() {
    $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true
    });
}

function removeClass(options_list) {
    var options = options_list
    for (var i = 0; i < options.length; i++) {
        $(options[i]).removeClass("active")
    }
}

function showAndHideRestCarousel(show_option) {
    var options_to_hide = [".popular", ".recent", ".oldest"]
    for (var i = 0; i < options_to_hide.length; i++) {
        $(options_to_hide[i]).hide()
    }
    $(show_option).show()
}

function carouselOptionsBehaviour(num_of_option) {
    $(".carousel_option" + String(num_of_option)).click(function() {
        if (!$(this).hasClass("active")) {
            if (num_of_option == 1) {
                removeClass([".carousel_option2", ".carousel_option3"])
                showAndHideRestCarousel(".popular")
                $("#carousel_options").val("1")
                refreshSelect()
            }
            else if (num_of_option == 2) {
                removeClass([".carousel_option1", ".carousel_option3"])
                showAndHideRestCarousel(".recent")
                $("#carousel_options").val("2")
                refreshSelect()
            }
            else {
                removeClass([".carousel_option1", ".carousel_option2"])
                showAndHideRestCarousel(".oldest")
                $("#carousel_options").val("3")
                refreshSelect()
            }
            $(this).addClass("active")
            refreshSlide()
        }
    });

    $("#carousel_options").change(function() {
        if ($(this).val() == 1) {
            removeClass([".carousel_option2", ".carousel_option3"])
            showAndHideRestCarousel(".popular")
            $(".carousel_option1").addClass("active")
        }
        else if ($(this).val() == 2) {
            removeClass([".carousel_option1", ".carousel_option3"])
            showAndHideRestCarousel(".recent")
            $(".carousel_option2").addClass("active")
        }
        else if ($(this).val() == 3) {
            removeClass([".carousel_option1", ".carousel_option2"])
            showAndHideRestCarousel(".oldest")
            $(".carousel_option3").addClass("active")
        }
        refreshSlide()
    })
}

function carouselArrows() {
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
    $(".add_ingredient").click(function() {
        $(".ingredients").append('<div class="input-field col s12 m11 offset-m1 another"><textarea name="instruction" class="materialize-textarea"></textarea></div>');
    });

    $(".remove_ingredient").click(function() {
        $(".ingredients .another:last-child").last().remove()
    })

    $(".add_instruction").click(function() {
        $(".instructions").append('<div class="input-field col s12 m11 offset-m1 another"><textarea name="ingredient" class="materialize-textarea"></textarea></div>');
    });

    $(".remove_instruction").click(function() {
        $(".instructions .another:last-child").last().remove()
    })
}

function collapsibleLists(selectors) {
    list_of_selectors = selectors
    for (var i = 0; i < list_of_selectors.length; i++) {
        $(list_of_selectors[i]).click(function() {
            if ($("#" + this.id + " i").hasClass("fa-chevron-down")) {
                $("#" + this.id + " i").removeClass("fa-chevron-down").addClass("fa-chevron-up")
            }
            else if ($("#" + this.id + " i").hasClass("fa-chevron-up")) {
                $("#" + this.id + " i").removeClass("fa-chevron-up").addClass("fa-chevron-down")
            }
            var list = this.nextElementSibling;
            if (list.style.maxHeight) {
                list.style.maxHeight = null;
            }
            else {
                list.style.maxHeight = list.scrollHeight + 100 + "px";
            }
        })
    }
}


function showAndHideRestProfile(show_option) {
    var options_to_hide = [".my_recipes", ".favourites"]
    for (var i = 0; i < options_to_hide.length; i++) {
        $(options_to_hide[i]).hide()
    }
    $(show_option).show()
}

function profileOptionsBehaviour(num_of_option) {
    $(".profile_option" + String(num_of_option)).click(function() {
        if (!$(this).hasClass("active")) {
            if (num_of_option == 1) {
                $(".profile_option2").removeClass("active")
                showAndHideRestProfile(".my_recipes")
                $("#profile_options").val("1")
                refreshSelect()
            }
            else if (num_of_option == 2) {
                $(".profile_option1").removeClass("active")
                showAndHideRestProfile(".favourites")
                $("#profile_options").val("2")
                refreshSelect()
            }
            $(this).addClass("active")
        }
    });

    $("#profile_options").change(function() {
        if ($(this).val() == 1) {
            $(".profile_option2").removeClass("active")
            showAndHideRestProfile(".my_recipes")
            $(".profile_option1").addClass("active")
        }
        else if ($(this).val() == 2) {
            $(".profile_option1").removeClass("active")
            showAndHideRestProfile(".favourites")
            $(".profile_option2").addClass("active")
        }
    })
}

function disableAndEnablePaginationArrows(pagination_class){
    if ($(pagination_class + " .num").first().hasClass("active")) {
        $(pagination_class + " .arrow").first().css('pointer-events', 'none')
        if (!$(pagination_class + " .arrow").first().hasClass("disabled")) {
            $(pagination_class + " .arrow").first().addClass("disabled")
        }
    } else {
        $(pagination_class + " .arrow").first().css('pointer-events', 'auto')
        if ($(pagination_class + " .arrow").first().hasClass("disabled")) {
            $(pagination_class + " .arrow").first().removeClass("disabled")
        }
    }
    
    if ($(pagination_class + " .num").last().hasClass("active")) {
        $(pagination_class + " .arrow").last().css('pointer-events', 'none')
        if (!$(pagination_class + " .arrow").last().hasClass("disabled")) {
            $(pagination_class + " .arrow").last().addClass("disabled")
        }
    } else {
        $(pagination_class + " .arrow").last().css('pointer-events', 'auto')
        if ($(pagination_class + " .arrow").last().hasClass("disabled")) {
            $(pagination_class + " .arrow").last().removeClass("disabled")
        }
    }
}
