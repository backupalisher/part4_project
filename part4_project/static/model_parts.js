$(document).ready(function () {
    $('#parts_search').keyup(function () {
        if ($(this).val().length > 1) {
            $('.module-title').removeClass('selected-module');
            const elems = $('.part-item_desc:contains('+ $(this).val().toUpperCase() +')' );
            if (elems.length > 0) {
                $id = elems.closest('.model-opts').first().attr('id');
                $('#'+$id+' .part-item').removeClass('active');
                document.getElementsByClassName($id)[0].click();
                $items = document.querySelectorAll('#'+$id+' .part-item')
                $items.forEach(x => {
                    if (x.innerHTML.indexOf($(this).val().toUpperCase()) > -1) {
                        x.classList.add('active')
//                        $('#'+$id).parent().parent().animate({
//                            scrollTop: x.offsetTop
//                        }, 200);
                    }
                });
            }
        } else {
            $('.part-item').removeClass('active');
            $('.part-item').addClass('active');
        }
    })
})