$(document).ready(function () {
    //Toggle themes
    if (Cookies.get('theme')) {
        if (Cookies.get('theme') === 'light-theme') {
            $('#body').removeClass('dark-theme')
            $('#body').addClass('light-theme')
        } else {
            $('#body').removeClass('light-theme')
            $('#body').addClass('dark-theme')
        }
    } else {
        $('#body').addClass('light-theme')
    }
    $('#toggle-theme').click(function () {
        if ($('#body').hasClass('dark-theme')) {
            $('#body').removeClass('dark-theme')
            $('#body').addClass('light-theme')
            Cookies.set('theme', 'light-theme', {expires: 365})
        } else {
            $('#body').removeClass('light-theme')
            $('#body').addClass('dark-theme')
            Cookies.set('theme', 'dark-theme', {expires: 365})
        }
    })
    $pathname = window.location.pathname;

    //Wait for element exist
    var waitForEl = function (selector, callback) {
        if (jQuery(selector).length) {
            callback();
        } else {
            setTimeout(function () {
                waitForEl(selector, callback);
            }, 100);
        }
    };

    var inProgress = false;
    var startFrom = 10;
    $('#to_up').click(function () {
        $('html, body').animate({scrollTop: 0}, 200);
    })
    $(window).scroll(function () {
        if ($(window).scrollTop() >= 200 && !$('#to_up').hasClass('visible')) {
            $('#to_up').addClass('visible')
        } else if ($(window).scrollTop() < 200 && $('#to_up').hasClass('visible')) {
            $('#to_up').removeClass('visible')
        }
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 200 && !inProgress) {
            inProgress = true;
            setTimeout(() => {
                startFrom += 10;
            }, 2000)
            inProgress = false;
        }
    });

    // Scrollbar
    jQuery(document).ready(function () {
        jQuery('.scrollbar-macosx').scrollbar();
    });


    //Search position and vals save
    if ($pathname.indexOf('search') > 0) {
        vals = getUrlVars($pathname)
        if (vals.length > 0) {
            localStorage.setItem('variant', vals['v'])
            localStorage.setItem('sval', decodeURIComponent(vals['s']))
        }
        if (localStorage.getItem('variant') && localStorage.getItem('sval')) {
            $v = localStorage.getItem('variant')
            $s = localStorage.getItem('sval').replace(/\+/g, ' ')
            $('#search_main .custom-select').val($v)
            $('#search_main input').val($s)
        }
    }

    // Brands
    // brands$ = $('.brands .brand').length
    // $('.brands').css('height', (brands$ - 1) * 134.5)
    $('.brands').css('height', $('.brands').parent().width())
    $( window ).resize(function() {
        $('.brands').css('height', $('.brands').parent().width())
    })

})

function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

// Model navs
$('#detailTabs a').click(function () {
    $id = $(this).attr('aria-controls')
    $('.tab-pane').removeClass('hide')
    $('.tab_controls a').removeClass('active')
    $('#controls_' + $id + '-tab').addClass('active')
})
$('.tab_controls a').click(function () {
    $id = $(this).attr('data-toggle')
    $href = $(this).attr('href')
    if ($(this).hasClass('active')) {
        $($href).toggleClass('hide')
        $(this).removeClass('active')
    } else {
        $('#' + $id).click()
    }
})

// Filter show/hide
$('#filter-title').click(function () {
    $('#filter_model').toggleClass('show')
})

// Change url
$('.nav-tabs a').click(function () {
    window.history.pushState('', '', $pathname + '?tab=' + $(this).attr('aria-controls'))
});

// Scroll horizontal
$(document).ready(function () {
    $('.brands').on('.brands', function (e, delta) {
        console.log(e, delta)
        this.scrollLeft -= (delta * 40);
        e.preventDefault();
    });
});

// error_result models toggle show
$('.error_result_models_show').click(function () {
    $('#' + $(this).attr('aria-label')).toggle()
    $(this).children('.btn_show').toggle()
    $(this).children('.btn_hide').toggle()
});

$('#btn-buy').click(function () {
    $('.main_overlay').toggleClass('active')
    $('.modal.contact').toggleClass('active')
    $('.c_form').css('display', 'block')
    $(".c_successful").removeClass('active')
});
$('#send_contact').click(function (event) {
    if ($('.c_name').val().length > 3 && ($('.c_phone').val().length > 8 || $('.c_email').val().length > 4)) {
        console.log(event)
        event.stopPropagation();
        event.preventDefault();
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            type: 'POST',
            url: '/sendmail/contact',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                "name": JSON.stringify($('.c_name').val()),
                "phone": JSON.stringify($('.c_phone').val()),
                "email": JSON.stringify($('.c_email').val()),
                'message': JSON.stringify($('.c_message').val()),
                'url': JSON.stringify(location.pathname),
            },
            contentType: "application/x-www-form-urlencoded;charset=utf-8",
            success: function (data) {
                $(".c_successful").toggleClass('active')
                $('.c_form').css('display', 'none')
            }
        });
    } else {
        console.log('invalid')
    }
})
$('.contact_close').click(function () {
    $('.main_overlay').toggleClass('active')
    $('.modal.contact').toggleClass('active')
});

// Show-hide filter
$('.filter_show').click(function () {
   $('.filter_show').toggleClass('active');
   $('#filter_model').toggleClass('active');
});

// Show-hide model list for search
$(document).on('click','.search_result_model button', function() {
    $('#'+$(this).val()).toggle()
});