$('.collapse').collapse()
$loading = false
$page_count = 0
page = 0
count = 40
aTop = $('#load_more').position().top;
if ($cartridges.length > 0) {
    $cartridges = $cartridges.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""')
    $cartridges = JSON.parse($cartridges)
    $page_count = Math.round($cartridges.length / count)
    $cartridges_all = $cartridges
    show_cartridges($cartridges_all, page, count)

}

if ($('#cartridge_items').length) {
    $(function () {
        if (page >= $page_count || $page_count === 1) {
            $('#load_more').toggleClass('hidden')
        } else {
            $('#load_more').toggleClass('hidden')
        }
        $('#cartridge_items').parent().parent().scroll(function () {
            if ($(this).scrollTop() + 1080 >= aTop) {
                if (!$loading && page < $page_count) {
                    $loading = true
                    page++
                    show_cartridges($cartridges_all, page, count)
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

function show_cartridges(cartridges, page, count) {
    for (let i = page * count; i < (page + 1) * count; i++) {
        if (cartridges[i]) {
            $html = '<div class="row"><div class="col-3"><a href="/cartridge/' + cartridges[i][0] + '" class="text-yellow">' + cartridges[i][1] + '</a></div>'
            if (cartridges[i][2]) {
                $html += '<div class="col-5"><span class="text-green">' + cartridges[i][2] + '</span></div>\n'
            } else if (cartridges[i][3]) {
                $html += '<div class="col-5"><span class="text-green">' + cartridges[i][3] + '</span></div>\n'
            }
            $html += '<div class="col-4">\n' +
                '<a class="btn_info" aria-controls="suppl' + i + '">i</a>\n' +
                '<div class="supplies-item" id="suppl' + i + '"><div class="supp-title">' + cartridges[i][1] + ' - '
            if (cartridges[i][2]) {$html += cartridges[i][2]}
            else if (cartridges[i][3]) {$html += cartridges[i][3]}
            $html += '</div> <h6>Analogs of models</h6> <div class="supplies-analogs">'
            if (cartridges[i][4]) {
                for (let ci = 0; ci < cartridges[i][4].length; ci++) {
                    if (cartridges[i][4][ci]) {
                        $html += cartridges[i][4][ci] + '<br>'
                    }
                }
            }
            if (cartridges[i][8]) {
                for (let cai = 0; cai < cartridges[i][8].length; cai++) {
                    if (cartridges[i][8][cai]) {
                        $html += cartridges[i][8][cai] + '<br>'
                    }
                }
            }
            $html += '</div><button type="button" aria-controls="suppl' + i + '">Close</button></div></div>'
            $('#cartridge_items').append($html)
        }
    }
    $loading = false
}

function search_cartridges(s) {
    $cartridges_all = []
    for (let i = 0; i < $cartridges.length; i++) {
        if ($cartridges[i][1].toLowerCase().indexOf(s.toLowerCase()) > -1 || $cartridges[i][2].toLowerCase().indexOf(s.toLowerCase()) > -1 || $cartridges[i][3].toLowerCase().indexOf(s.toLowerCase()) > -1) {
            $cartridges_all.push($cartridges[i])
        }
    }
    page = 0
    aTop = $('#load_more').position().top;
    show_cartridges($cartridges_all, page, count)
}

$('#cartridge_search').keyup(function () {
    let sval = $(this).val()
    if (sval.length > 2) {
        $('#cartridge_items').html('')
        search_cartridges(sval)
    } else {
        $cartridges_all = $cartridges
        $('#cartridge_items').html('')
        show_cartridges($cartridges_all, page, count)
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
    window.location.href = '/cartridge/?brand='+$brand_id
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
$(document).on('click','#cartridge_items .btn_info', function() {
    $('.supplies-item').removeClass('active')
    $('#'+$(this).attr('aria-controls')).addClass('active')
})

// Close supplies popup
$(document).on('click','#cartridge_items button', function() {
    $('.supplies-item').removeClass('active')
    $('#'+$(this).attr('aria-controls')).removeClass('active')
})
