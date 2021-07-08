// String to json
function toJSON(item) {
    item = item.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\\/g, '/').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    return JSON.parse(item)
}

module = toJSON(module)[0]

function module_show() {
    if (module.length > 0) {
        $inner_html = '<h4><small>module: </small>' + module[1] + '</h4><form class="form-floating">' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="module_name_en" value="' + module[1] + '">' +
            '<label for="module_name_en">Name en:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="module_name_ru" value="' + module[2] + '">' +
            '<label for="module_name_ru">Name ru:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<button class="btn btn-success save" value="' + module[0] + '">save</button>' +
            '</div>' +
            '</form>'
        $('#module_item').html($inner_html)
    }
}

$(document).on('click', '.save', function (event) {
    $(this).addClass('disabled')
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.stopPropagation();
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/dashboard/modules',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "action": 'save',
            "module_id": $(this).val(),
            "name_ru": $('#module_name_ru').val(),
            "name_en": $('#module_name_en').val(),
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            $("#module_item").html('').append(data);
            $('.save').removeClass('disabled')
        }
    });
})

module_show();