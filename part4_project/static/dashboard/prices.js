// String to json
function toJSON(item) {
    item = item.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\\/g, '/').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    return JSON.parse(item)
}

if (prices.length > 0) {
    prices = toJSON(prices)
}
if (models.length > 0) {
    models = toJSON(models)
}
if (vendors.length > 0) {
    vendors = toJSON(vendors)
    console.log(vendors)
}


$('#search_prices').keyup(function (event) {
    val = $(this).val().toLowerCase()
    if (val.length > 2 && event.keyCode === 13) {
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            type: 'POST',
            url: '/dashboard/prices',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                "action": 'search_price',
                "val": val,
            },
            contentType: "application/x-www-form-urlencoded;charset=utf-8",
            success: function (data) {
                $("#prices_list").html('').append(data);
            }
        });
    } else {

    }
});

$('#search_add').keyup(function (event) {
    val = $(this).val().toLowerCase()
    if (val.length > 2) {
        smodels = models.filter(x => x[1].toLowerCase().indexOf(val) > -1)
        $html = ''
        smodels.forEach(item => {
            $html += '<button type="button" class="btn btn-link btn_new_price" area_type="model" ' +
                'value="' + item[0] + '">' + item[1] + '</button>'
        })
        $('#select_list').append().html($html)
    } else {
        smodels = models
    }
    if (val.length > 3 && event.keyCode === 13) {
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            type: 'POST',
            url: '/dashboard/prices',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                "action": 'search_add',
                "val": val,
            },
            contentType: "application/x-www-form-urlencoded;charset=utf-8",
            success: function (data) {
                console.log(data)
                $("#select_list").html('').append(data);
            }
        });
    } else {

    }
});

$(document).on('click', '.btn_new_price', function (event) {
    event.stopPropagation();
    event.preventDefault();
    $('.btn_new_price').removeClass('disabled');
    $(this).addClass('disabled');
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log($(this).val())
    $.ajax({
        type: 'POST',
        url: '/dashboard/prices',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "action": 'new_price',
            "id": $(this).val(),
            "type": $(this).attr('area_type'),
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            $("#price_item").html('').append(data);
        }
    });
});

$(document).on('click', '.btn_price', function (event) {
    event.stopPropagation();
    event.preventDefault();
    $('.btn_price').removeClass('disabled');
    $(this).addClass('disabled');
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log($(this).val())
    $.ajax({
        type: 'POST',
        url: '/dashboard/prices',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "action": 'show_price',
            "id": $(this).val(),
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            $("#price_item").html('').append(data);
        }
    });
})