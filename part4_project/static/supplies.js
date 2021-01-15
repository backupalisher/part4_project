$(document).ready(function () {
    //Toggle phone and email
    $('#toggle-order').click(function () {
        $('.order-form').toggle()
    })

    $('#submit-order').click(function () {
        $form = getFormData($('.order-form form'));
        $.ajax({
            type: 'POST',
            url: '/sendmail/',
            data: {
                'csrfmiddlewaretoken': $form.csrfmiddlewaretoken,
                'title': $form.title,
                'product_code': $form.product_code,
                'product_id': $form.product_id,
                'email': $form.email,
                'phone': $form.phone,
                'name': $form.name,
            }
        }).done(function (response) {
            console.log(response); // if you're into that sorta thing
        });
    })

    $('.phone-toggle').click(function () {
        $('.phone-toggle').toggle()
        $('.phone').toggle()
    })
    $('.email-toggle').click(function () {
        $('.email-toggle').toggle()
        $('.email').toggle()
    })
})

function getFormData($form) {
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function (n, i) {
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}