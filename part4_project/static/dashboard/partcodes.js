partcodes = partcodes.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
partcodes = JSON.parse(partcodes)


$('#search_partcodes').keyup(function () {
    val = $(this).val().toLowerCase()
    if (val.length > 2) {
        spartcode = partcodes.filter(x => x[1].toLowerCase().indexOf(val) > -1)
        $html = ''
        spartcode.forEach(item => {
            $html += '<button type="button" class="btn btn-link btn_partcode" value="' + item[0] + '">' + item[1] + '</button>'
        })
        $('#parcode_list').append().html($html)
    } else {
        spartcode = partcodes
    }
});

$(document).on('click', '.btn_partcode', function (event) {
    event.stopPropagation();
    event.preventDefault();
    $('.btn_partcode').removeClass('disabled');
    $(this).addClass('disabled');
    pid = $(this).val();
    console.log(pid);
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
             $("#detail_item").html('').append(
                data
            );
        }
    });
})