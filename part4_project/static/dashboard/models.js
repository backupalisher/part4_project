function toJSON(item) {
    item = item.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\\/g, '/').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    return JSON.parse(item)
}

models = toJSON(models)

$(document).on('click', '.btn_show_model', function (event) {
    event.stopPropagation();
    event.preventDefault();
    $('.btn_show_model').removeClass('disabled');
    $(this).addClass('disabled');
    mid = $(this).attr('model_id');
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: 'POST',
        url: '/dashboard/models',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "mid": mid,
            "action": 'show_model',
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            $("#model_detail_result").html('').append(
                data
            );
        }
    });
})

$('#model_search').keyup(function () {
    let val = $(this).val().toLowerCase();
    if (val.length > 2) {
        smodels = models.filter(x => x[1].toLowerCase().indexOf(val) > -1)
        $html = ''
        smodels.forEach(item => {
            $html += '<button type="button" class="btn btn-link btn_show_model" value="' + item[1] + '" ' +
                'model_id="' + item[0] + '">' + item[1] + '</button>'
        })
        $('#model_list').append().html($html)
    } else {
        smodels = models
    }
})

