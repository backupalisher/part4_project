// partcodes = partcodes.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
// partcodes = JSON.parse(partcodes)


$('#search_partcodes').keyup(function (event) {
    val = $(this).val().toLowerCase()
    if (val.length > 3 && event.keyCode === 13) {
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            type: 'POST',
            url: '/dashboard/partcodes',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                "val": val,
                "action": 'search_partcode',
            },
            contentType: "application/x-www-form-urlencoded;charset=utf-8",
            success: function (data) {
                $('#parcode_list').html('').append(data);
            }
        });
    } else {

    }
});

$(document).on('click', '.btn_partcode', function (event) {
    event.stopPropagation();
    event.preventDefault();
    $('.btn_partcode').removeClass('disabled');
    $(this).addClass('disabled');
    pid = $(this).val();
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: 'POST',
        url: '/dashboard/partcodes',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "pid": pid,
            "action": 'show_partcode',
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            $("#detail_item").html('').append(data);
        }
    });
})