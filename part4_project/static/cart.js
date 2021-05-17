/* Show modal contact form on buy
$('#btn-buy, .hide_contact').click(function () {
    $('.main_overlay').toggleClass('active')
    $('.modal.contact').toggleClass('active')
    $('.c_form').css('display', 'block')
    $(".c_successful").removeClass('active')
});
*/

if ($cart_items.length > 0) {
    $cart_items = $cart_items.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '').replace(/datetime.date/g, '')
    $cart_items = JSON.parse($cart_items)
}

// Add to cart
$('#btn-buy').click(function () {
    change_cart($(this).val(), 'add', '')
})

$(".cart_item_remove").click(function () {
    change_cart($(this).attr('id'), 'remove', '')
})

$('.cart_counter .cart_plus').click(function () {
    if ($(this).parent().children('input').val() < $(this).parent().attr('counts')) {
        change_cart($(this).attr('aria-id'), 'count', 'plus')
        $(this).parent().children('input').val(parseInt($(this).parent().children('input').val()) + 1)
    }
})

$('.cart_counter .cart_minus').click(function () {
    if ($(this).parent().children('input').val() > 1) {
        change_cart($(this).attr('aria-id'), 'count', 'minus')
        $(this).parent().children('input').val(parseInt($(this).parent().children('input').val()) - 1)
    }
})

$('.cart_order .btn').click(function () {
    $('.main_overlay').addClass('active');
    $('.cart_order_modal').addClass('active');
})

$('.main_overlay, .cart_modal_close').click(function () {
    $('.main_overlay').removeClass('active');
    $('.cart_order_modal').removeClass('active');
})

function change_cart($pid, $action, $value) {
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let jdata = {}
    if ($action === 'add') {
        jdata = {
            "changecart": true,
            "action": "add",
            "pid": $pid,
        }
    } else if ($action === 'remove') {
        jdata = {
            "changecart": true,
            "action": "remove",
            "pid": $pid,
        }
    } else if ($action === 'count') {
        jdata = {
            "changecart": true,
            "action": "count",
            "value": $value,
            "pid": $pid,
        }
    }
    $.ajax({
        type: 'POST',
        url: '',
        headers: {'X-CSRFToken': csrftoken},
        data: jdata,
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            if ($action === 'add') {
                $('.cart_block').html('').append(data)
            } else {
                $('.cart_wrap').html('').append(data)
            }
        }
    });
}


$('#cart_order').click(function () {
    order();
})

function order() {
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $summ = $('.cart_sum span').html()
    $first_name = $('#first_name').val()
    $last_name = $('#last_name').val()
    $email = $('#email').val()
    $address = $('#address').val()
    $phone = $('#phone').val()
    items = []
    $cart_items.forEach(e => {
        items.push({
            'cart_id': e[0],
            'orders': e[2].trim(),
            'count': e[3],
            'price': e[4][0].trim(),
            'partcode_id': e[5],
            'model_id': e[6],
            'vendor_id': e[9]
        })
    })
    jdata = {
        "order": true,
        "first_name": $first_name,
        "last_name": $last_name,
        "email": $email,
        "address": $address,
        "phone": $phone,
        "cart_items": JSON.stringify(items),
        "summ": $summ
    }
    $.ajax({
        type: 'POST',
        url: '',
        headers: {'X-CSRFToken': csrftoken},
        data: jdata,
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            $('.cart_wrap').html('').append(data)
        }
    });
}