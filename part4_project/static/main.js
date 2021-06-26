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
        $('#body').addClass('dark-theme')
    }
    $('.toggle-theme').click(function () {
        console.log('toggle-theme')
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

    // Toggle language
    $('#language_select label').click(function () {
        $('#language_select .custom-select').toggleClass('active')
    })

    // Wait for element exist
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
    // $('.brands').css('height', $('.brands').parent().width())
    // $( window ).resize(function() {
    //     $('.brands').css('height', $('.brands').parent().width())
    // })

    // Active ursl
    $('#filters h2').removeClass('active')
    $('#filters h2 span').removeClass('active')
    $('.filter').removeClass('active')
    if ($pathname.indexOf('market') > 0) {
        $('#nav_market').parent().addClass('active')
        $('.filter_market').addClass('active')
    } else if ($pathname.indexOf('supplies') > 0) {
        $('#nav_consumables').parent().addClass('active')
        $('.filter_partcodes').addClass('active')
    } else if ($pathname.indexOf('about') > 0) {
        $('#nav_about').parent().addClass('active')
    } else {
        $('#nav_models').parent().addClass('active')
        $('.filter_model').addClass('active')
    }
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

// Show-hide main menu
$('.btn_menu').click(function () {
    $('.btn_menu').toggleClass('active');
    $('.top_menu').toggleClass('active');
})

// Show hide main search
$('.btn_search').click(function () {
    $('.form_search').toggleClass('active');
})

// Nav's set active
$(document).ready(function () {
    $('.nav-item').removeClass('active');
    if ($pathname.indexOf('model') > 0) {
        $('.nav-item.models').addClass('active');
    } else if ($pathname.indexOf('partcodes') > 0) {
        $('.nav-item.consumables').addClass('active');
    } else if ($pathname.indexOf('market') > 0) {
        $('.nav-item.market').addClass('active');
    } else {
        $('.nav-item.models').addClass('active');
    }
})

// Show hide filter
$('.btn_filter, .btn_close_filter').click(function() {
    $('aside').toggleClass('active');
})

// Expand modules
$('.parts_module').click(function() {
    $(this).toggleClass('active')
})

$('.module-title').click(function() {
    $text = $(this).html()
    $('#selected_module').html($text)
})


// Show hide account menu
$('.account_btn').click(function () {
    $('.account_menu').toggleClass('active')
})

