let $brands = []
$(document).ready(function () {
    let userLang = navigator.language || navigator.userAgent;
    let media_url = "{{ MEDIA_URL }}"
    let $loading = false
    let $page_count = 0
    let $checkboxs = {}
    let $tcheckboxs = {}
    let $ranges = {}
    let $tranges = {}
    let $radios = {}
    let $tradios = {}

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
        checkDisable($('.filter_settings').offset().top + 75);
        $("#form_filter #submit").trigger('click');
    });


    // Ajax filter
    if ($('.filter_model').length) {
        $("#form_filter #reset").click(function () {
            $("#reset").removeClass('active');
            $("#filter_badge").removeClass('active').html('');
            $checkboxs = {}
            $tcheckboxs = {}
            $ranges = {}
            $tranges = {}
            $radios = {}
            $tradios = {}
            $brands = []
            $('.brand label').removeClass('checked');
            $('.filter_settings label').removeClass('checked');
            $("form").trigger("reset");
            $('.loading').addClass('active');
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
                    $('.loading').removeClass('active');
                    $('.filter_search').addClass('is_filtered')
                }
            });
            checkDisable(0);
            $('#filter_badge').removeClass('active');
        })
        $("#form_filter #submit, #form_filter #float").click(function (event) {
            if (Object.keys($checkboxs).length > 0 || Object.keys($ranges).length > 0 || Object.keys($radios).length > 0 || $brands.length > 0) {
                $('.loading').addClass('active');
                $('.not-found').removeClass('active');
                $('#float').css('top', $('.filter_settings').offset().top).css('display', 'none');
                $inHtml = ''
                $.each($tcheckboxs, function (key, arr) {
                    for (let i = 0; i < arr.length / 3; i++) {
                        $inHtml += '<div class="fbadge" key="' + key.replace(arr[i * 3], '') + '" id="' + key + '" type="' + arr[1 + i * 3] + '">'
                            + arr[2 + i * 3] + '</div>'
                    }
                });
                $.each($tranges, function (key, arr) {
                    $inHtml += '<div class="fbadge" key="' + key + '"  id="' + key + arr[0] + '" type="' + arr[1] + '">'
                        + arr[0] + ' ' + arr[2] + '</div>'
                });
                $.each($tradios, function (key, arr) {
                    $inHtml += '<div class="fbadge" key="' + key + '"  id="' + key + arr[0] + '" type="' + arr[1] + '">' + arr[2] + '</div>'
                });
                $('#filter_badge').addClass('active').html($inHtml);
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
                        $('.loading').removeClass('active');
                        $('.filter_search').addClass('is_filtered');
                        if (data.trim().length > 712) {
                            $('.not-found').removeClass('active');
                        } else {
                            $('.not-found').addClass('active');
                        }
                    }
                });
            } else {
                document.getElementById('reset').click();
            }
        })
    }

    $(document).on('click', '.fbadge', function () {
        $key = $(this).attr('key');
        $id = $(this).attr('id').replace($key, '');
        $type = $(this).attr('type');
        console.log($type, $id, $key)
        if ($type === 'number') {
            $(this).remove();
            document.getElementsByName($key+'min')[0].value = '';
            document.getElementsByName($key+'max')[0].value = '';
            delete $ranges[$key]
            $("#form_filter #float").click();
        } else {
            document.getElementById($id).click();
        }
    });

    // Filter change
    $("#form_filter input").change(function () {
        change_input($(this));
    });

    function checkDisable(pos) {
        if (pos === 0) {
            $('#float').css('top', pos - 15 - $('.filter_settings').offset().top).css('display', 'none');
        } else {
            $('#float').css('top', pos - 15 - $('.filter_settings').offset().top).css('display', 'block');
        }
        $('.filter_model a.btn').removeClass("disabled");
    }

    function change_input(el) {
        if (el.parent().parent().hasClass('brand')) {
            $("#reset").addClass('active')
            $key = el.attr('name');
            $value = el.attr('id');
            $title = el.parent().text().replace(/ +/g, ' ').trim();
            $.extend($tcheckboxs, {[$key + $value]: [$value, el.attr('type'), $title]})
            $('#form_filter #float').trigger('click');
        } else {
            switch (el.attr('type')) {
                case 'checkbox':
                    el.parent().toggleClass('checked');
                    $key = el.attr('name');
                    $value = el.attr('id');
                    $title = el.parent().text().replace(/ +/g, ' ').trim();
                    set_array($key, $value, el.attr('type'), $title, '');
                    break;
                case 'number':
                    $key = el.attr('name')
                    $value = el.val()
                    $title = el.parent().parent().parent().children('h6').text() + ' ' + el.parent().text().replace(/ +/g, ' ').trim()
                    set_array($key, $value, el.attr('type'), $title, '')
                    break;
                case 'radio':
                    sname = el.attr("name")
                    _radios = $('input[name~="' + sname + '"]')
                    _checked = false
                    _id0 = _radios[0]['id']
                    _id1 = _radios[1]['id']
                    if ($('input[id~=' + _id0 + ']').parent().hasClass('checked') ||
                        $('input[id~=' + _id1 + ']').parent().hasClass('checked')) {
                        $('input[id~=' + _id0 + ']').parent().toggleClass('checked')
                        $('input[id~=' + _id1 + ']').parent().toggleClass('checked')
                    } else {
                        el.parent().addClass('checked')
                    }
                    $key = el.attr('name')
                    $value = el.attr('id')
                    $title = el.parent().parent().parent().children('h6').text() + ' ' + el.parent().text().replace(/ +/g, ' ').trim()
                    set_array($key, $value, el.attr('type'), $title, '')
                    break;
            }
        }
        checkDisable(el.offset().top);
    }

    function set_array(key, value, type, title, action) {
        console.log(key, value, type, title, action)
        $("#reset").addClass('active')
        $("#filter_badge").addClass('active')
        $newelem = {[key]: value}
        switch (type) {
            case 'checkbox':
                if (action === 'remove') {
                    delete $checkboxs[key]
                    delete $tcheckboxs[key + value]
                } else {
                    if (Object.getOwnPropertyNames($checkboxs).length === 0) {
                        $.extend($checkboxs, {[key]: [value]})
                        $.extend($tcheckboxs, {[key + value]: [value, type, title]})
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
                            delete $tcheckboxs[idx + value];
                        } else if (idx !== '') {
                            $checkboxs[idx].push(value)
                            $.extend($tcheckboxs, {[key + value]: [value, type, title]})
                        } else {
                            $.extend($checkboxs, {[key]: [value]})
                            $.extend($tcheckboxs, {[key + value]: [value, type, title]})
                        }
                    }
                }

                $.each($checkboxs, function (k, v) {
                    if (v.length < 1) {
                        delete $checkboxs[k]
                        delete $tcheckboxs[k + v]
                    }
                });
                // console.log($checkboxs);
                // console.log($tcheckboxs);
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
                        $.extend($tranges, {[key.replace('min', '')]: [value, type, title]})
                    } else if (max !== '') {
                        $.extend($ranges, {[max]: [0]})
                        $ranges[max].push(parseInt(value, 10))
                        $.extend($tranges, {[key.replace('max', '')]: [value, type, title]})
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
                            $tranges[idx.replace('max', '')] = [value, type, title]
                        } else {
                            $.extend($ranges, {[min]: [parseInt(value, 10)]})
                            $ranges[min].push(0)
                            $.extend($tranges, {[key.replace('min', '')]: [value, type, title]})
                        }
                    } else if (max !== '') {
                        $.each($ranges, function (key, arr) {
                            if (key === max) {
                                idx = key
                            }
                        })
                        if (idx !== '') {
                            $ranges[idx][1] = parseInt(value, 10)
                            $tranges[idx.replace('max', '')] = [value, type, title]
                        } else {
                            $.extend($ranges, {[max]: [0]})
                            $ranges[max].push(parseInt(value, 10))
                            $.extend($tranges, {[key.replace('max', '')]: [value, type, title]})
                        }
                    }
                }
                if (action === 'remove') {
                    delete $tranges[key]
                    delete $ranges[key]
                }
                // console.log($tranges);
                break;
            case 'radio':
                if (Object.getOwnPropertyNames($radios).length === 0) {
                    $.extend($radios, $newelem)
                    $.extend($tradios, {[key]: [value, type, title]})
                } else {
                    let idx = ''
                    $.each($radios, function (k, item) {
                        if (key === k) {
                            idx = k
                        }
                    })
                    if (idx !== '') {
                        $radios[idx] = value;
                        if (action === 'remove') {
                            delete $tradios[idx];
                        } else {
                            $tradios[idx] = [value, type, title];
                        }
                    } else {
                        $.extend($radios, $newelem)
                        $.extend($tradios, {[key]: [value, type, title]})
                    }
                }
                // console.log($tradios);
                break;
        }
        $('#form_filter #float').trigger('click')
    }
})
