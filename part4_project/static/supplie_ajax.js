$('.collapse').collapse()
$loading = false
$page_count = 0
page = 0
count = 40
aTop = $('#load_more').position().top;
if ($supplies.length > 0) {
    $supplies = $supplies.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    console.log($supplies)
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
    for (let i = page * count; i < (page + 1) * count; i++) {
        if (supplies[i]) {
            $html = '<div class="row"><div class="col-3"><a href="/supplies/' + supplies[i][0] + '" class="">' + supplies[i][1] + '</a></div>'
            if (supplies[i][2]) {
                $html += '<div class="col-5"><span class="">' + supplies[i][2] + '</span></div>\n'
            } else if (supplies[i][3]) {
                $html += '<div class="col-5"><span class="">' + supplies[i][3] + '</span></div>\n'
            }
            $html += '<div class="col-4">\n' +
                '<a class="btn_info" aria-controls="suppl' + i + '">i</a>\n' +
                '<div class="main_overlay suppl' + i + '"></div><div class="supplies-item" id="suppl' + i + '"><div class="supp-title">' + supplies[i][1] + ' - '
            if (supplies[i][2]) {$html += supplies[i][2]}
            else if (supplies[i][3]) {$html += supplies[i][3]}
            $html += '</div> <h6>Analogs of models</h6> <div class="supplies-analogs">'
            if (supplies[i][4]) {
                for (let ci = 0; ci < supplies[i][4].length; ci++) {
                    if (supplies[i][4][ci]) {
                        $html +='<a href="/model/' + supplies[i][5][ci] + '" >' + supplies[i][4][ci] + '</a><br>'
                    }
                }
            }
            if (supplies[i][8]) {
                $html += '<hr>'
                for (let cai = 0; cai < supplies[i][8].length; cai++) {
                    if (supplies[i][8][cai]) {
                        $html += supplies[i][8][cai] + '<br>'
                    }
                }
            }
            $html += '</div><button type="button" aria-controls="suppl' + i + '">Close</button></div></div>'
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

// Change brand checks
$('.brand label input').click(function () {
    $brand_id = $(this).val()
    if ($(this).parent().hasClass('checked')) {
        $(this).parent().toggleClass('checked');
        $brand_id = 0;
    } else {
        $('.brand label').removeClass('checked')
        $(this).parent().addClass('checked');
    }
    window.location.href = '/supplies/?brand='+$brand_id
})

// Add brand check status on load page
var $brand_id = getUrlVars()['brand']
$('.brand label input[name="'+ $brand_id +'"]').parent().addClass('checked')

function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

// Open supplies popup
$(document).on('click','#supplie_items .btn_info', function() {
    $('.supplies-item').removeClass('active')
    $('#'+$(this).attr('aria-controls')).addClass('active')
    $('.'+$(this).attr('aria-controls')).addClass('active')
})

// Close supplies popup
$(document).on('click','#supplie_items button', function() {
    $('.supplies-item').removeClass('active')
    $('#'+$(this).attr('aria-controls')).removeClass('active')
    $('.'+$(this).attr('aria-controls')).removeClass('active')
})
