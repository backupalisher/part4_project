/* Show modal contact form on buy
$('#btn-buy, .hide_contact').click(function () {
    $('.main_overlay').toggleClass('active')
    $('.modal.contact').toggleClass('active')
    $('.c_form').css('display', 'block')
    $(".c_successful").removeClass('active')
});
*/


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
