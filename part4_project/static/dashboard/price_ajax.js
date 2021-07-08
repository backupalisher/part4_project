// String to json
function toJSON(item) {
    item = item.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\\/g, '/').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    return JSON.parse(item)
}

if (price.length > 0 && price !== 'new') {
    price = toJSON(price)[0]
}
if (models.length > 0) {
    models = toJSON(models)
}
if (vendors.length > 0) {
    vendors = toJSON(vendors)
}

loading = true;

function price_show() {
    if (price === 'new') {
        $inner_html = '<h4><small>Price for </small>' + title + '</h4><form class="form-floating">' +
            '<div class="form-floating mb-3">' +
            '<input type="number" class="form-control" id="price" value="">' +
            '<label for="price">Price:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<select class="form-select" id="vendor">'
                for (let i = 0; i < vendors.length; i++) {
                    $inner_html += '<option value="' + vendors[i][0] + '">' + vendors[i][1] + '</option>'
                    }
                $inner_html += '</select><label for="vendor">Vendor:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="usage_status" value="">' +
            '<label for="usage_status">Usage status:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="description" value="">' +
            '<label for="description">Description:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="images" value="">' +
            '<label for="images">Images:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="number" class="form-control" id="count" value="">' +
            '<label for="count">Count:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<button class="btn btn-success save" value="' + nid + '" data_type="'+ptype+'">save</button></div></form>'
    } else if (price.length > 0) {
        $inner_html = '<h4><small>Price: </small>' + price[2] + '/ ' + price[0] + price[1] + '</h4><form class="form-floating">' +
            '<div class="form-floating mb-3">' +
            '<input type="number" class="form-control" id="price" value="' + price[3][0] + '">' +
            '<label for="price">Price:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<select class="form-select" id="vendor">'
                for (let i = 0; i < vendors.length; i++) {
                    $inner_html += '<option value="' + vendors[i][0] + '"'
                    if (price[4] === vendors[i][1]) {
                        $inner_html += ' selected>' + vendors[i][1] + '</option>'
                    } else {
                        $inner_html += '>' + vendors[i][1] + '</option>'
                    }
                }
                $inner_html += '</select><label for="vendor">Vendor:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="usage_status" value="' + price[7] + '">' +
            '<label for="usage_status">Usage status:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="description" value="' + price[9] + '">' +
            '<label for="description">Description:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="images" value="' + price[10] + '">' +
            '<label for="images">Images:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="number" class="form-control" id="count" value="' + price[11] + '">' +
            '<label for="count">Count:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<button class="btn btn-success save" value="' + price[8] + '" data_type="save">save</button></div></form>'
    }
    $('#price_item').html($inner_html)
}

$(document).on('click', '.save', function (event) {
    $(this).addClass('disabled')
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.stopPropagation();
    event.preventDefault();
    if ($(this).attr('data_type') === 'save') {
        $data = {
            "action": 'save',
            "id": $(this).val(),
            "price": $('#price').val(),
            "vendor_id": $('#vendor').val(),
            "usage_status": $('#usage_status').val(),
            "description": $('#description').val(),
            "images": $('#images').val(),
            "count": $('#count').val(),
        }
    } else {
        $data = {
            "action": 'add_price',
            "id": $(this).val(),
            "price": $('#price').val(),
            "vendor_id": $('#vendor').val(),
            "usage_status": $('#usage_status').val(),
            "description": $('#description').val(),
            "images": $('#images').val(),
            "count": $('#count').val(),
            "type": ptype,
        }
    }
    if (loading) {
        loading = false;
        $.ajax({
            type: 'POST',
            url: '/dashboard/prices',
            headers: {'X-CSRFToken': csrftoken},
            data: $data,
            contentType: "application/x-www-form-urlencoded;charset=utf-8",
            success: function (data) {
                $("#price_item").html('').append(data);
                $('.save').removeClass('disabled');
                loading = true;
            }
        });
    }

})

price_show();