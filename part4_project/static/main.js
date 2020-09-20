$(document).ready(function () {
    let userLang = navigator.language || navigator.userAgent;
    let brand_models = ""
    let media_url = "{{ MEDIA_URL }}"
    let $loading = false
    let $page_count = 0
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
        $('html, body').animate( { scrollTop: 0 }, 200 );
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

    //Scrollbar
    jQuery(document).ready(function () {
        jQuery('.scrollbar-macosx').scrollbar();
    });



    // Ajax filter
    if ($('#filter_model').length) {
        $checkboxs = {}
        $ranges = {}
        $radios = {}
        $("#form_filter input").change(function () {
            console.log('change')
            if ($(this).attr('type') === 'checkbox') {
                $key = $(this).attr('name')
                $value = $(this).attr('id')
                set_array($key, $value, $(this).attr('type'))
            }
            if ($(this).attr('type') === 'number') {
                $key = $(this).attr('name')
                $value = $(this).val()
                set_array($key, $value, $(this).attr('type'))
            }
            if ($(this).attr('type') === 'radio') {
                $key = $(this).attr('name')
                $value = $(this).attr('id')
                set_array($key, $value, $(this).attr('type'))
            }

            function set_array(key, value, type) {
                // console.log(key, value, type)
                $newelem = {[key]: value}
                switch (type) {
                    case 'checkbox':
                        if (Object.getOwnPropertyNames($checkboxs).length === 0) {
                            $.extend($checkboxs, {[key]: [value]})
                        } else {
                            let idx = ''
                            let index = null
                            $.each($checkboxs, function (k, v) {
                                if (key === k) {
                                    idx = k
                                    if (Array.isArray(v)) {
                                        $.each(v, function (i, val) {
                                            if (val === value) {
                                                index = i
                                            }
                                        })
                                    }
                                }
                            })
                            console.log(idx)
                            if (idx !== '' && index !== null) {
                                $checkboxs[idx].splice(index, 1);
                            } else if (idx !== '') {
                                $checkboxs[idx].push(value)
                                // $.extend($checkboxs, val)
                            } else {
                                $.extend($checkboxs, {[key]: [value]})
                            }
                        }
                        break;
                    case 'number':
                        let min = ''
                        let max = ''
                        if (key.indexOf('min') > 0) {
                            min = key.replace('min', '')
                        }
                        if (key.indexOf('max') > 0) {
                            max = key.replace('max', '')
                        }
                        if (Object.getOwnPropertyNames($ranges).length === 0) {
                            if (min !== '') {
                                $.extend($ranges, {[min]: [parseInt(value, 10)]})
                                $ranges[min].push(0)
                            } else if (max !== '') {
                                $.extend($ranges, {[max]: [0]})
                                $ranges[max].push(parseInt(value, 10))
                            }
                        } else {
                            let idx = ''
                            if (min !== '') {
                                $.each($ranges, function (key, arr) {
                                    if (key === min) {
                                        idx = key
                                    }
                                })
                                if (idx !== '') {
                                    $ranges[idx][0] = parseInt(value, 10)
                                } else {
                                    $.extend($ranges, {[min]: [parseInt(value, 10)]})
                                    $ranges[min].push(0)
                                }
                            } else if (max !== '') {
                                $.each($ranges, function (key, arr) {
                                    if (key === max) {
                                        idx = key
                                    }
                                })
                                if (idx !== '') {
                                    $ranges[idx][1] = parseInt(value, 10)
                                } else {
                                    $.extend($ranges, {[max]: [0]})
                                    $ranges[max].push(parseInt(value, 10))
                                }
                            }
                        }
                        console.log($ranges)
                        break
                    case 'radio':
                        if (Object.getOwnPropertyNames($radios).length === 0) {
                            $.extend($radios, $newelem)
                        } else {
                            let idx = ''
                            $.each($radios, function (k, item) {
                                if (key === k) {
                                    idx = k
                                }
                            })
                            if (idx !== '') {
                                $radios[idx] = value;
                            } else {
                                $.extend($radios, $newelem)
                            }
                        }
                        break
                }
            }
            console.log($checkboxs)
            console.log($ranges)
            console.log($radios)

            if (Object.keys($checkboxs).length > 0 || Object.keys($ranges).length > 0 || Object.keys($radios).length > 0) {
                $('#filter_model a.btn').removeClass("disabled");
            } else {
                $('#filter_model a.btn').addClass("disabled");
            }
        })
        $("#form_filter #reset").click(function () {
            $checkboxs = {}
            $ranges = {}
            $radios = {}
            $("form").trigger("reset");
        })
        $("#form_filter #submit").click(function (event) {
            if (Object.keys($checkboxs).length > 0 || Object.keys($ranges).length > 0 || Object.keys($radios).length > 0) {
                console.log('test')
                event.preventDefault();
                let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                $.ajax({
                    type: 'POST',
                    url: '',
                    headers: {'X-CSRFToken': csrftoken},
                    data: {
                        "checkboxs": JSON.stringify($checkboxs),
                        "ranges": JSON.stringify($ranges),
                        "radios": JSON.stringify($radios)
                    },
                    contentType: "application/x-www-form-urlencoded;charset=utf-8",
                    success: function (data) {
                        $("#filter_model_result").html('').append(
                            data
                        );
                    }
                });
            }
        })
    }


    //Toggle themes
    $('#toggle-theme').click(function () {
        console.log('change')
        if ($('#body').hasClass('dark-theme')) {
            $('#body').removeClass('dark-theme')
            $('#body').addClass('light-theme')
        } else {
            $('#body').removeClass('light-theme')
            $('#body').addClass('dark-theme')
        }
    })

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

    // if ($pathname.indexOf('brands') > 0) {
    //     $("form").submit(function (event) {
    //             /* Serialize the submitted form control values to be sent to the web server with the request */
    //             let formValues = $(this).serialize();
    //             // Stop form from submitting normally
    //             event.preventDefault();
    //             let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    //             $.ajax({
    //                 type: 'POST',
    //                 url: '',
    //                 csrfmiddlewaretoken: csrftoken,
    //                 headers: {'X-CSRFToken': csrftoken},
    //                 data: {formValues},
    //                 success: function (data) {
    //                     $("#brands").html('').append(
    //                         data
    //                     );
    //                 }
    //             });
    //         }
    //     )
    // }
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
    $('#controls_'+$id+'-tab').addClass('active')
})
$('.tab_controls a').click(function () {
    $id = $(this).attr('data-toggle')
    $href = $(this).attr('href')
    if ($(this).hasClass('active')) {
        $($href).toggleClass('hide')
        $(this).removeClass('active')
    } else {
        $('#'+$id).click()
    }
})

// Filter show/hide
$('#filter-title').click(function () {
    $('#filter_model').toggleClass('show')
})