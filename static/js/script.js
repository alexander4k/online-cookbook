$(document).ready(function() {
    $(".recent").hide()
    $(".least_popular").hide()
    $('.sidenav').sidenav();
    
    refreshSlide()
    refreshSelect()
    
    slideCursorToGrab()
    changeLikeIconAndCursor()
    
    slideOptionsBehaviour(1)
    slideOptionsBehaviour(2)
    slideOptionsBehaviour(3)
});

function slideCursorToGrab(){
    $(".recipe_slide").on({
        mousedown: function() {
            $(this).css("cursor", "grabbing");
        },
        mouseup: function() {
            $(this).css("cursor", "grab");
        }
    });
}

function changeLikeIconAndCursor(){
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

function slideOptionsBehaviour(num_of_option) {
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
