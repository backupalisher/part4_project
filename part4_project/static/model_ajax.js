$loading = false
$page_count = 0
page = 0
count = 24
$models_all = []
aTop = 0
if (brand_models.length > 0) {
    brand_models = toJSON(brand_models)
    $page_count = Math.round(brand_models.length / count)
    $models_all = brand_models
    show_models($models_all, media_url, page, count)
}


if ($('.card-model-list').length) {
    $(function () {
        aTop = $('#load_more').position().top;
        if (page >= $page_count || $page_count === 1) {
            $('#load_more').toggleClass('hidden')
        } else {
            $('#load_more').toggleClass('hidden')
        }
        $('.card-model-list').parent().parent().scroll(function () {
            if ($(this).scrollTop() + 1080 >= aTop) {
                if (!$loading && page < $page_count) {
                    $loading = true
                    page++
                    show_models($models_all, media_url, page, count)
                    aTop += 1080
                }
                if (page >= $page_count) {
                    $('#load_more').toggleClass('hidden')
                } else {
                    $('#load_more').toggleClass('hidden')
                }
            }
        });
    });
}

function show_models(models, media_url, page, count) {
    for (let i = page * count; i < (page + 1) * count; i++) {
        if (models[i]) {
            console.log(models[i][8][0])
            $priced = ''
            $desc = ''
            if (models[i][3] !== "") {
                $mstyle = 'style="background-image:url(\'' + media_url + models[i][3] + '\');"'
            } else {
                $mstyle = 'style="background-image:url(\'' + media_url + 'no_image.svg\'); background-size: 80%;"'
            }
            if (models[i][8][0]) {
                if (lang === 'ru') {
                    $priced = '<p class="model_price">' + models[i][8][0] + ' &#x20bd;</p>'
                } else {
                    $priced = '<p class="model_price">$' + Math.round(parseInt(models[i][8][0], 10) / parseInt(currency, 10)) + '</p>'
                }
            }
            if (models[i][10]) {
                models[i][10].forEach(el => {
                    if (el.indexOf('Status') > -1) {
                        $desc = '<p class="status">' + el.replace('Status: ', '') + '</p>'
                    }
                })
                models[i][10].forEach(el => {
                    if (el.indexOf('Status') > -1) {

                    } else if (/^([A][4])/g.test(el)) {
                        $desc += '<p>' + el.replace('A4', 'Скорость печати A4') +'</p>'
                    } else {
                        $desc += '<p>' + el +'</p>'
                    }
                })
            }
            $html = '<div class="card card-model-item btn">' +
                    '<a href="/model/' + models[i][0] + '" class="card_model_link">' +
                    '<div class="card-image" ' + $mstyle + '></div>' +
                    '<div class="card-desc">' +
                    '<h4>' + models[i][1] + '</h4>' + $desc + $priced + '</div></a></div>'

            $('.card-model-list .row').append($html)
        }
    }
    $loading = false
}

//Filter by model name
function filter_search(s) {
    $models_all = []
    for (let i = 0; i < brand_models.length; i++) {
        if (brand_models[i][1].toLowerCase().indexOf(s.toLowerCase()) > -1) {
            $models_all.push(brand_models[i])
        }
    }
    page = 0
    show_models($models_all, media_url, page, count)
}

$('#filter_search').keyup(function () {
    let sval = $(this).val()
    if (sval.length > 2) {
        $('.card-model-list .row').html('')
        filter_search(sval)
    } else {
        $models_all = brand_models
        $('.card-model-list .row').html('')
        aTop = $('#load_more').position().top;
        show_models($models_all, media_url, 0, count)
    }
})
$('#filter_search_clear').click(function () {
    $models_all = brand_models
    $('.card-model-list .row').html('')
    aTop = $('#load_more').position().top;
    show_models($models_all, media_url, 0, count)
    $('#filter_search').val('')
})


// String to json
function toJSON(item) {
    item = item.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\\/g, '/').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    return JSON.parse(item)
}