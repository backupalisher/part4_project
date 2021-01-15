// String to json
function toJSON(item) {
    item = item.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\\/g, '/').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    return JSON.parse(item)
}

details = toJSON(details)

$('#search_details').keyup(function () {
    val = $(this).val().toLowerCase()
    if (val.length > 2) {
        sdetails = details.filter(x => x[2].toLowerCase().indexOf(val) > -1)
        $html = ''
        sdetails.forEach(item => {
            $html += '<button type="button" class="btn btn-link btn_detail" value="' + item[0] + '">' + item[2] + '</button>'
        })
        $('#details_list').append().html($html)
    } else {
        sdetails = details
    }
});

$(document).on('click', '.btn_detail', function (event) {
    event.stopPropagation();
    event.preventDefault();
    $('.btn_detail').removeClass('disabled');
    $(this).addClass('disabled');
    did = $(this).val();
    console.log(did);
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: 'POST',
        url: '/dashboard/details',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "did": did,
            "action": 'show_detail',
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
             $("#detail_item").html('').append(
                data
            );
        }
    });
})