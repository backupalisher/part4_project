$brands = []
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

// Change brand checks
$('.brands label input').click(function () {
    $(this).parent().toggleClass('checked')
    $(this).checked = true
    if ($brands.length > 0) {
        idx = $brands.indexOf(parseInt($(this).val()))
        if (idx < 0) {
            $brands.push(parseInt($(this).val()))
        } else {
            $brands.splice(idx, 1)
        }
    } else {
        $brands.push(parseInt($(this).val()))
    }
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: 'POST',
        url: '',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "reset": JSON.stringify(false),
            'brands': JSON.stringify($brands)
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            // console.log(data)
            $(".supplies_wrap").html('').append(
                data
            );
        }
    });
})