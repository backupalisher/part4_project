// document.addEventListener('DOMContentLoaded', function(){
    $loading = false
    $page_count = 0
    if (brand_models.length > 0){
        brand_models = brand_models.replace(/&#x27;/g,"'")
        brand_models = brand_models.replace(/'/g,'"')
        brand_models = brand_models.replace(/\(/g,'[')
        brand_models = brand_models.replace(/\)/g,']')
        brand_models = brand_models.replace(/None/g,'""')
        brand_models = JSON.parse(brand_models)
        $page_count = Math.round(brand_models.length/24)
        show_models(brand_models, media_url,0, 24)

    }


    if($('.card-model-list').length) {
        $(function(){
          let page = 0
          let aTop = $('#load_more').position().top;
          if(page >= $page_count || $page_count === 1){
            $('#load_more').toggleClass('hidden')
          } else {
            $('#load_more').toggleClass('hidden')
          }
          $('.card-model-list').parent().parent().scroll(function(){
            if($(this).scrollTop()+1080>=aTop){
                if(!$loading && page < $page_count) {
                    $loading = true
                    page++
                    show_models(brand_models, media_url,page, 24)
                    aTop += 1080
                }
                if(page >= $page_count){
                    $('#load_more').toggleClass('hidden')
                } else {
                    $('#load_more').toggleClass('hidden')
                }
            }
          });
        });
    }
// })

function show_models(models, media_url, page, count) {
    for(let i = page*count; i < (page+1)*count; i++) {
        if(models[i]) {
            if(models[i][4] !== "") {
                $mstyle = 'style="background-image:url(\''+media_url+models[i][4]+'\')"'
            } else {
                $mstyle = 'style="background-image:url(\''+media_url+'no-image.png\')"'
            }
            $html = '<div class="col-lg-3 col-md-4 col-sm-6 p-2"> <div class="card card-model-item btn">' +
                '<a href="/model/'+models[i][1]+'" class="brand_model_link" ' + $mstyle +'>' +
                '<div class="brand_model_title">'+models[i][2]+'</div></a>' +
                '</div></div>'
            $('.card-model-list .row').append($html)
        }
    }
    $loading = false
}




