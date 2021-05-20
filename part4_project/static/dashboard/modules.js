// String to json
function toJSON(item) {
    item = item.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\\/g, '/').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    return JSON.parse(item)
}

modules = toJSON(modules)
console.log(modules)

$('#search_modules').keyup(function () {
    val = $(this).val().toLowerCase()
    console.log(val)
    if (val.length > 2) {
        smodules = modules.filter(x => x[1].toLowerCase().indexOf(val) > -1)
        $html = ''
        smodules.forEach(item => {
            $html += '<button type="button" class="btn btn-link btn_module" value="' + item[0] + '">' + item[1] + '</button>'
        })
        $('#modules_list').append().html($html)
    } else {
        smodules = modules
    }
});

$(document).on('click', '.btn_module', function (event) {
    event.stopPropagation();
    event.preventDefault();
    $('.btn_module').removeClass('disabled');
    $(this).addClass('disabled');
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: 'POST',
        url: '/dashboard/modules',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "module_id": $(this).val(),
            "action": 'show_module',
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
             $("#module_item").html('').append(data);
        }
    });
})