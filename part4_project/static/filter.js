let $brands = []
$(document).ready(function () {
    let userLang = navigator.language || navigator.userAgent;
    let brand_models = ""
    let media_url = "{{ MEDIA_URL }}"
    let $loading = false
    let $page_count = 0

    // Brands checkbox

    $('.brand label input').click(function () {
        if ($brands.length > 0) {
            idx = $brands.indexOf(parseInt($(this).val()))
            if (idx < 0) {
                $brands.push(parseInt($(this).val()))
            } else {
                $brands.splice(idx, 1)
            }
        } else {
            $brands.push(parseInt($(this).val()))
        }
        $(this).parent().toggleClass('checked');
        checkDisable();
    });

    // Filter
    $('#form_filter label input[type="checkbox"]').click(function () {
        $(this).parent().toggleClass('checked')
    });
    $('#form_filter label input[type="radio"]').click(function () {
        sname = $(this).attr("name")
        _radios = $('input[name~="' + sname + '"]')
        _checked = false
        _id0 = _radios[0]['id']
        _id1 = _radios[1]['id']
        for (let i = 0; i < _radios.length; i++) {
            if ($('input[id~=' + _id0 + ']').parent().hasClass('checked')) {
                _checked = true
            }
            if ($('input[id~=' + _id1 + ']').parent().hasClass('checked')) {
                _checked = true
            }
        }
        if (!_checked) {
            $(this).parent().addClass('checked')
        } else {
            $('input[id~=' + _id0 + ']').parent().toggleClass('checked')
            $('input[id~=' + _id1 + ']').parent().toggleClass('checked')
        }
    });

    // Ajax filter
    if ($('#filter_model').length) {
        $checkboxs = {}
        $ranges = {}
        $radios = {}
        $("#form_filter input").change(function () {
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
                            if (idx !== '' && index !== null) {
                                $checkboxs[idx].splice(index, 1);
                            } else if (idx !== '') {
                                $checkboxs[idx].push(value)
                                // $.extend($checkboxs, val)
                            } else {
                                $.extend($checkboxs, {[key]: [value]})
                            }
                        }
                        $.each($checkboxs, function (k, v) {
                            if (v.length < 1) {
                                console.log($checkboxs[k])
                                delete $checkboxs[k]
                            }
                        });
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

            checkDisable();
        })
        $("#form_filter #reset").click(function () {
            $checkboxs = {}
            $ranges = {}
            $radios = {}
            $brands = []
            $('.brand label').removeClass('checked');
            $('.filter_settings label').removeClass('checked');
            $("form").trigger("reset");
            let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            $.ajax({
                type: 'POST',
                url: '',
                headers: {'X-CSRFToken': csrftoken},
                data: {
                    "reset": JSON.stringify(true),
                },
                contentType: "application/x-www-form-urlencoded;charset=utf-8",
                success: function (data) {
                    $("#filter_model_result").html('').append(
                        data
                    );
                    $('.filter_search').addClass('is_filtered')
                }
            });
            checkDisable();
        })
        $("#form_filter #submit").click(function (event) {
            if (Object.keys($checkboxs).length > 0 || Object.keys($ranges).length > 0 || Object.keys($radios).length > 0 || $brands.length > 0) {
                event.preventDefault();
                let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                if ($brands.length < 1) {
                    $fbrands = null
                } else {
                    $fbrands = $brands
                }
                $.ajax({
                    type: 'POST',
                    url: '',
                    headers: {'X-CSRFToken': csrftoken},
                    data: {
                        "reset": JSON.stringify(false),
                        "checkboxs": JSON.stringify($checkboxs),
                        "ranges": JSON.stringify($ranges),
                        "radios": JSON.stringify($radios),
                        'brands': JSON.stringify($fbrands)
                    },
                    contentType: "application/x-www-form-urlencoded;charset=utf-8",
                    success: function (data) {
                        $("#filter_model_result").html('').append(
                            data
                        );
                        $('.filter_search').addClass('is_filtered')
                    }
                });
            }
        })
    }
})

function checkDisable() {
    $('#filter_model a.btn').removeClass("disabled");
    // if (Object.keys($checkboxs).length > 0 || Object.keys($ranges).length > 0 || Object.keys($radios).length > 0 || $brands.length > 0) {
    //     $('#filter_model a.btn').removeClass("disabled");
    // } else {
    //     $('#filter_model a.btn').addClass("disabled");
    // }
}