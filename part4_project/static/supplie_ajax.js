// $('.collapse').collapse()
$loading = false
$page_count = 0
page = 0
count = 40
aTop = $('#load_more').position().top;
if ($partcodes.length > 0) {
    $partcodes = $partcodes.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    $partcodes = JSON.parse($partcodes)
    $page_count = Math.round($partcodes.length / count)
    $partcodes_all = $partcodes
    show_partcodes($partcodes_all, page, count)
}

if ($('#partcode_items .row').length) {
    $(function () {
        if (page >= $page_count || $page_count === 1) {
            $('#load_more').toggleClass('hidden')
        } else {
            $('#load_more').toggleClass('hidden')
        }
        $('#partcode_items .row').parent().parent().parent().scroll(function () {
            if ($(this).scrollTop() + 1080 >= aTop) {
                if (!$loading && page < $page_count) {
                    $loading = true
                    page++
                    show_partcodes($partcodes_all, page, count)
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

function show_partcodes(partcodes, page, count) {
    let $modal;
    let $html;
    let $image;
    let $desc;
    for (let i = page * count; i < (page + 1) * count; i++) {
        if (partcodes[i]) {
            $html = '<div class="partcodes-item">'
            $image = '<div class="partcode_image">'
            if (partcodes[i][3]) {
                $image += '<img src=""' + $media_url + partcodes[i][3] + '" alt=""/>'
            } else {
                $image += '<img src="' + $media_url + 'no_image.svg" alt=""/>'
            }
            $image += '</div>'

            $desc = '<div class="partcode_desc"><p><a href="/partcode/' + partcodes[i][0] + '" class="partcodes_code">' + partcodes[i][1] + '</a> '
                if (partcodes[i][12]) {
                    $desc += '<a class="btn_info" aria-controls="suppl' + i + '"><span class="material-icons">info</span></a>'
                }
                $desc += '</p>'
            if (partcodes[i][6] && $lang === 'ru') {
                $desc += '<h4>' + partcodes[i][6] + '</h4>'
            }
            if (partcodes[i][5]) {
                $desc += '<h4>' + partcodes[i][5] + '</h4>'
            }
            $desc += '</div>'

            $modal = ''
            if (partcodes[i][12]) {
                $modal = '<div class="main_overlay suppl' + i + '"></div>' +
                    '<div class="partcodes-item_overlay" id="suppl' + i + '"><div class="supp-title">' + partcodes[i][1] + ' - '
                if (partcodes[i][5]) {
                    $modal += partcodes[i][5]
                } else if (partcodes[i][6]) {
                    $modal += partcodes[i][6]
                }
                $modal += '</div> <h3>Analogs of models:</h3> <div class="partcodes-analogs">'
                for (let ci = 0; ci < partcodes[i][12].length; ci++) {
                    if (partcodes[i][12][ci]) {
                        $modal += '<a href="/model/' + partcodes[i][12][ci].split('~')[0] + '" >' +
                            partcodes[i][12][ci].split('~')[1] + '</a><br>'
                    }
                }
                $modal += '</div><div class="btm_modal_close"><button type="button" aria-controls="suppl' + i + '">' +
                    '<span class="material-icons-outlined">close</span></button></div></div></div>'
            }
            $html += $image + $desc + $modal + '</div>'
            $('#partcode_items .row').append($html)
        }
    }
    $loading = false
}

function search_partcodes(s) {
    $partcodes_all = []
    for (let i = 0; i < $partcodes.length; i++) {
        if ($partcodes[i][1].toLowerCase().indexOf(s.toLowerCase()) > -1 || $partcodes[i][5].toLowerCase().indexOf(s.toLowerCase()) > -1 || $partcodes[i][6].toLowerCase().indexOf(s.toLowerCase()) > -1) {
            $partcodes_all.push($partcodes[i])
        }
    }
    page = 0
    aTop = $('#load_more').position().top;
    show_partcodes($partcodes_all, page, count)
}

$('#supplie_search').keyup(function () {
    let sval = $(this).val()
    if (sval.length > 2) {
        $('#partcode_items .row').html('')
        search_partcodes(sval)
    } else {
        $partcodes_all = $partcodes
        $('#partcode_items .row').html('')
        aTop = $('#load_more').position().top;
        show_partcodes($partcodes_all, 0, 40)
    }
})

// Open partcodes popup
$(document).on('click', '#partcode_items .btn_info', function () {
    $('.partcodes-item').removeClass('active')
    $('#' + $(this).attr('aria-controls')).addClass('active')
    $('.' + $(this).attr('aria-controls')).addClass('active')
})

// Close partcodes popup
$(document).on('click', '#partcode_items button', function () {
    $('.partcodes-item').removeClass('active')
    $('#' + $(this).attr('aria-controls')).removeClass('active')
    $('.' + $(this).attr('aria-controls')).removeClass('active')
})
