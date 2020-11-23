$(document).ready(function () {
    $('#parts_search').keyup(function () {
        if ($(this).val().length > 1) {
            const elem = $('a:contains('+ $(this).val().toUpperCase() +')' );
            if (elem.length > 0) {
                $id = elem.closest('.model-opts').first().attr('id');
                $('#'+$id+' .part-item').removeClass('active');
                document.getElementsByClassName($id)[0].click();
                $items = document.querySelectorAll('#'+$id+' .part-item')
                $items.forEach(x => {
                    if (x.innerHTML.indexOf($(this).val().toUpperCase()) > -1) {
                        x.classList.add('active')
                        $('#'+$id).parent().parent().animate({
                            scrollTop: x.offsetTop
                        }, 200);
                    }
                });
            }
        } else {

        }
    })
})