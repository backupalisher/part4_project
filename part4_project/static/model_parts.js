$(document).ready(function () {
    $('#parts_search').keyup(function () {
        if ($(this).val().length > 1) {
            const elem = $('a:contains('+ $(this).val().toUpperCase() +')' );
            if (elem.length > 0) {
                $id = elem.closest('.model-opts').first().attr('id');
                document.getElementsByClassName($id)[0].click();
            }
        } else {

        }
    })
})