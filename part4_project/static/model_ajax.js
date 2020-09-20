$loading = false
$page_count = 0
page = 0
count = 24
$models_all = []
if (brand_models.length > 0) {
    brand_models = brand_models.replace(/&#x27;/g, "'")
    brand_models = brand_models.replace(/'/g, '"')
    brand_models = brand_models.replace(/\(/g, '[')
    brand_models = brand_models.replace(/\)/g, ']')
    brand_models = brand_models.replace(/None/g, '""')
    brand_models = JSON.parse(brand_models)
    $page_count = Math.round(brand_models.length / count)
    $models_all = brand_models
    show_models($models_all, media_url, page, count)

}


if ($('.card-model-list').length) {
    $(function () {
        let aTop = $('#load_more').position().top;
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
            if (models[i][4] !== "") {
                $mstyle = 'style="background-image:url(\'' + media_url + models[i][4] + '\')"'
            } else {
                $mstyle = 'style="background-image:url(\'' + media_url + 'no-image.png\')"'
            }
            $html = '<div class="col-lg-3 col-md-4 col-sm-6 p-2"> <div class="card card-model-item btn">' +
                '<a href="/model/' + models[i][1] + '" class="brand_model_link" ' + $mstyle + '>' +
                '<div class="brand_model_title">' + models[i][2] + '</div></a>' +
                '</div></div>'
            $('.card-model-list .row').append($html)
        }
    }
    $loading = false
}

//Filter by model name
function filter_search(s) {
    $models_all = []
    for (let i = 0; i < brand_models.length; i++) {
        if (brand_models[i][2].toLowerCase().indexOf(s.toLowerCase()) > -1) {
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
        show_models($models_all, media_url, page, count)
    }
})
$('#filter_search_clear').click(function () {
    $models_all = brand_models
    $('.card-model-list .row').html('')
    show_models($models_all, media_url, page, count)
})


