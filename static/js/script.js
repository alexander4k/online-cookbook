$(document).ready(function() {
    $(".recent").hide()
    $(".least_popular").hide()
    $('.sidenav').sidenav();
    $('.tooltipped').tooltip();
    refreshSlide()
    refreshSelect()
    changeLikeIconAndCursor()
    addAndRemoveElements()
    carouselArrows()
    carouselOptionsBehaviour(1)
    carouselOptionsBehaviour(2)
    carouselOptionsBehaviour(3)
    collapsibleLists(["#ingredients_expand",
                      "#instructions_expand",
                      "#allergens_expand",
                      "#nutrition_expand"])

});

function changeLikeIconAndCursor() {
    $(".fa-star").on({
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

function showAndHideRest(show_option) {
    var options_to_hide = [".popular", ".recent", ".least_popular"]
    for (var i = 0; i < options_to_hide.length; i++) {
        $(options_to_hide[i]).hide()
    }
    $(show_option).show()
}

function carouselOptionsBehaviour(num_of_option) {
    $(".option" + String(num_of_option)).click(function() {
        if (!$(this).hasClass("active")) {
            if (num_of_option == 1) {
                removeClass([".option2", ".option3"])
                showAndHideRest(".popular")
                $("#options").val("1")
                refreshSelect()
            }
            else if (num_of_option == 2) {
                removeClass([".option1", ".option3"])
                showAndHideRest(".recent")
                $("#options").val("2")
                refreshSelect()
            }
            else {
                removeClass([".option1", ".option2"])
                showAndHideRest(".least_popular")
                $("#options").val("3")
                refreshSelect()
            }
            $(this).addClass("active")
            refreshSlide()
        }
    });

    $("#options").change(function() {
        if ($(this).val() == 1) {
            removeClass([".option2", ".option3"])
            showAndHideRest(".popular")
            $(".option1").addClass("active")
        }
        else if ($(this).val() == 2) {
            removeClass([".option1", ".option3"])
            showAndHideRest(".recent")
            $(".option2").addClass("active")
        }
        else if ($(this).val() == 3) {
            removeClass([".option1", ".option2"])
            showAndHideRest(".least_popular")
            $(".option3").addClass("active")
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
            if($("#" + this.id + " i").hasClass("fa-chevron-down")){
                $("#" + this.id + " i").removeClass("fa-chevron-down").addClass("fa-chevron-up")
            } else if($("#" + this.id + " i").hasClass("fa-chevron-up")) {
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




