// String to json
function toJSON(item) {
    item = item.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\\/g, '/').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    return JSON.parse(item)
}

function detail_show() {
    if (partcode.length > 0) {
        brands = toJSON(brands)
        partcode = toJSON(partcode)
        vendors = toJSON(vendors)
        $inner_html = '<h4><small>partcode: </small>' + partcode[0][0][1] + '</h4><form class="form-floating">\n' +
            '<div class="form-floating mb-3">\n' +
            '<input type="text" class="form-control" id="partcode_desc" value="' + partcode[0][0][2] + '">\n' +
            '<label for="partcode_desc">Description:</label>\n' +
            '</div>' +
            '<div class="form-floating mb-3">\n' +
            '<input type="text" class="form-control" id="partcode_image" placeholder="" value="' + partcode[0][0][3] + '">\n' +
            '<label for="partcode_image">Image:</label>\n' +
            '</div>\n' +
            '<div class="form-floating mb-3">\n' +
            '<input type="text" class="form-control" id="partcode_article" placeholder="" value="' + partcode[0][0][4] + '">\n' +
            '<label for="partcode_article">Article:</label>\n' +
            '</div>' +
            '<div class="form-floating mb-3">' +
            '<select class="form-select" id="vendor_price">' +
            '<option value="">---</option>'
        for (let i = 0; i < vendors.length; i++) {
            $inner_html += '<option value="' + vendors[i][0] + '"'
            if (partcode[1][0]) {
                if (partcode[1][0][1] === vendors[i][0]) {
                    $inner_html += ' selected>'
                } else {
                    $inner_html += ' >'
                }
            } else {
                $inner_html += ' >'
            }
            $inner_html += vendors[i][1] + '</option>'
        }
        $inner_html += '</select>' +
            '<label for="vendor_price">Vendor:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="detail_price"'
        if (partcode[1][0]) {
            $inner_html += 'value="' + partcode[1][0][0] + '"'
        }
        if (partcode[1][0]) {
            $inner_html += 'vendor="' + partcode[1][0][1] + '"'
        }
        $inner_html += '><label for="detail_price">Price:</label></div>'
        if (partcode[1][0]) {
            $inner_html += '<input type="hidden" id="price_id" value="' + partcode[1][0][2] + '">'
        }
        $inner_html += '<div class="form-floating mb-3">' +
            '<button class="btn btn-success save" value="' + partcode[0][0][0] + '">save</button>' +
            '</div></form>'

        $('#partcode_item').html($inner_html)
    }
}

$(document).on('click', '.save', function (event) {
    $(this).addClass('disabled')
    pid = $(this).val()
    partcode_desc = $('#partcode_desc').val()
    partcode_image = $('#partcode_image').val()
    partcode_article = $('#partcode_article').val()
    detail_price = $('#detail_price').val()
    vendor = $('#vendor_price').val()
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.stopPropagation();
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/dashboard/partcodes',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "action": 'save',
            "pid": pid,
            "partcode_desc": partcode_desc,
            "partcode_image": partcode_image,
            "partcode_article": partcode_article,
            "detail_price": detail_price,
            "vendor": vendor,
            "price_id": $('#price_id').val()
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            $('.save').removeClass('disabled')
        }
    });
})

detail_show();