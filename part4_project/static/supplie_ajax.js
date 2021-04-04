// $('.collapse').collapse()
$loading = false
$page_count = 0
page = 0
count = 40
aTop = $('#load_more').position().top;

if ($supplies.length > 0) {
    $supplies = $supplies.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    $supplies = JSON.parse($supplies)
    $page_count = Math.round($supplies.length / count)
    $supplies_all = $supplies
    show_supplies($supplies_all, page, count)
}

if ($('#supplie_items').length) {
    $(function () {
        if (page >= $page_count || $page_count === 1) {
            $('#load_more').toggleClass('hidden')
        } else {
            $('#load_more').toggleClass('hidden')
        }
        $('#supplie_items').parent().parent().scroll(function () {
            if ($(this).scrollTop() + 1080 >= aTop) {
                if (!$loading && page < $page_count) {
                    $loading = true
                    page++
                    show_supplies($supplies_all, page, count)
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

function show_supplies(supplies, page, count) {
    let $modal;
    let $html;
    let $image;
    let $desc;
    for (let i = page * count; i < (page + 1) * count; i++) {
        if (supplies[i]) {
            $html = '<div class="supplies-item">'
            $image = '<div class="supplie_image">'
            if (supplies[i][3]) {
                $image += '<img src=""' + $media_url + supplies[i][3] + '" alt=""/>'
            } else {
                $image += '<img src="' + $media_url + 'no_image.svg" alt=""/>'
            }
            $image += '</div>'

            $desc = '<div class="supplie_desc"><p>Manufacturer\'s code: ' +
                '<a class="btn_info" aria-controls="suppl' + i + '"><span class="material-icons">info</span></a></p> ' +
                '<a href="/supplies/' + supplies[i][0] + '" class="">' + supplies[i][1] + '</a>' +
                '<p>Title:</p>'
            if (supplies[i][6] && $lang === 'ru') {
                $desc += '<h4>' + supplies[i][6] + '</h4>'
            }
            if (supplies[i][5]) {
                $desc += '<h4>' + supplies[i][5] + '</h4>'
            }
            $desc += '</div>'

            $modal = ''
            if (supplies[i][12]) {
                $modal = '<div class="main_overlay suppl' + i + '"></div>' +
                    '<div class="supplies-item_overlay" id="suppl' + i + '"><div class="supp-title">' + supplies[i][1] + ' - '
                if (supplies[i][5]) {
                    $modal += supplies[i][5]
                } else if (supplies[i][6]) {
                    $modal += supplies[i][6]
                }
                $modal += '</div> <h3>Analogs of models:</h3> <div class="supplies-analogs">'
                for (let ci = 0; ci < supplies[i][12].length; ci++) {
                    if (supplies[i][12][ci]) {
                        $modal += '<a href="/model/' + supplies[i][12][ci].match(/^.*:/)[0].replace(":", "") + '" >' +
                            supplies[i][12][ci].match(/:.*/)[0].replace(":", "") + '</a><br>'
                    }
                }
                $modal += '</div><div class="justify-center"><button type="button" aria-controls="suppl' + i + '">Close</button></div></div></div>'
            }
            $html += $image + $desc + $modal + '</div>'
            $('#supplie_items').append($html)
        }
    }
    $loading = false
}

function search_supplies(s) {
    $supplies_all = []
    for (let i = 0; i < $supplies.length; i++) {
        if ($supplies[i][1].toLowerCase().indexOf(s.toLowerCase()) > -1 || $supplies[i][2].toLowerCase().indexOf(s.toLowerCase()) > -1 || $supplies[i][3].toLowerCase().indexOf(s.toLowerCase()) > -1) {
            $supplies_all.push($supplies[i])
        }
    }
    page = 0
    aTop = $('#load_more').position().top;
    show_supplies($supplies_all, page, count)
}

$('#supplie_search').keyup(function () {
    let sval = $(this).val()
    if (sval.length > 2) {
        $('#supplie_items').html('')
        search_supplies(sval)
    } else {
        $supplies_all = $supplies
        $('#supplie_items').html('')
        aTop = $('#load_more').position().top;
        show_supplies($supplies_all, 0, 40)
    }
})

// Open supplies popup
$(document).on('click', '#supplie_items .btn_info', function () {
    $('.supplies-item').removeClass('active')
    $('#' + $(this).attr('aria-controls')).addClass('active')
    $('.' + $(this).attr('aria-controls')).addClass('active')
})

// Close supplies popup
$(document).on('click', '#supplie_items button', function () {
    $('.supplies-item').removeClass('active')
    $('#' + $(this).attr('aria-controls')).removeClass('active')
    $('.' + $(this).attr('aria-controls')).removeClass('active')
})
