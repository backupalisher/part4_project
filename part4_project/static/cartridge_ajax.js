// document.addEventListener('DOMContentLoaded', function(){
$('.collapse').collapse()
$loading = false
$page_count = 0
if ($cartridges.length > 0) {
    $cartridges = $cartridges.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""')
    $cartridges = JSON.parse($cartridges)
    $page_count = Math.round($cartridges.length / 40)
    show_cartridges($cartridges, $media_url, 0, 40)

}

if ($('#cartridge_items').length) {
    $(function () {
        let page = 0
        let aTop = $('#load_more').position().top;
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
                    show_cartridges($cartridges, $media_url, page, 40)
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

// })

function show_cartridges(cartridges, media_url, page, count) {
    for(let i = page*count; i < (page+1)*count; i++) {
        if(cartridges[i]) {
            $html = '<div class="row"><div class="col-3"><a href="/cartridge/'+cartridges[i][0]+'" class="text-yellow">'+cartridges[i][1]+'</a></div>'
            if(cartridges[i][2]) {
                $html += '<div class="col-5"><span class="text-green">'+cartridges[i][2]+'</span></div>\n'
            } else if(cartridges[i][3]) {
                $html += '<div class="col-5"><span class="text-green">'+cartridges[i][3]+'</span></div>\n'
            }
            $html +='<div class="col-4"><div class="accordion">\n' +
                '<a class="btn-collapse text-grey" data-toggle="collapse" data-target="#collapse'+i+'" ' +
                'aria-expanded="false" aria-controls="collapse'+i+'">Показать модели</a>\n' +
                '<div class="collapse" id="collapse'+i+'"><div class="">\n'
            if(cartridges[i][4]) {
                for(let ci = 0; ci < cartridges[i][4].length; ci++){
                    $html += cartridges[i][4][ci]+'<br>'
                }
            }
            if(cartridges[i][8]) {
                for(let cai = 0; cai < cartridges[i][8].length; cai++){
                    $html += cartridges[i][8][cai]+'<br>'
                }
            }
            $html +='</div></div></div></div></div>'
            $('#cartridge_items').append($html)
        }
    }
    $loading = false
}



