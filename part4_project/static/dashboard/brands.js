$('.save').click(function (event) {
    $(this).addClass('disabled')
    id = $(this).attr('id')
    console.log(id)
    name = $('#name'+id).val()
    logotype = $('#logotype'+id).val()
    console.log(id, name, logotype)
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.stopPropagation();
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/dashboard/brands',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "id": id,
            "name": name,
            "logotype": logotype,
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            console.log('success')
            $('#'+id).removeClass('disabled')
        }
    });
})