// String to json
function toJSON(item) {
    item = item.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\\/g, '/').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    return JSON.parse(item)
}

partcodes = toJSON(partcodes)

function detail_show() {
    if (detail.length > 0) {
        detail = toJSON(detail)
        vendors = toJSON(vendors)
        console.log(detail)
        $inner_html = '<h4><small>partcode: </small>' + detail[2] + ' (' + detail[7] + ')</h4><form class="form-floating">' +
            '<input type="hidden" id="spr_id" value="' + detail[1] + '">' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="detail_name" value="' + detail[3] + '">' +
            '<label for="detail_name">Name in ru:</label>' +
            '</div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="description" value="' + detail[4] + '">' +
            '<label for="description">Description:</label>' +
            '</div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="seo" value="' + detail[5] + '">' +
            '<label for="seo">Seo:</label>' +
            '</div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="base_img" value="' + detail[6] + '">' +
            '<label for="base_img">Base image:</label>' +
            '</div>' +
            '<div class="form-floating mb-3">' +
            '<select class="form-select" id="vendor_price">' +
            '<option value="' + detail[11] + '">---</option>'
        for (let i = 0; i < vendors.length; i++) {
            $inner_html += '<option value="' + vendors[i][0] + '"'
            if (detail[11] === vendors[i][0]) {
                $inner_html += ' selected>'
            } else {
                $inner_html += ' >'
            }
            $inner_html += vendors[i][1] + '</option>'
        }
        $inner_html += '</select>' +
            '<label for="vendor_price">Vendor:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="detail_price"'
        if (detail[9]) {
            $inner_html += 'value="' + detail[9] + '"'
        }
        $inner_html += '><label for="detail_price">Price:</label></div>' +
            '<input type="hidden" id="price_id" value="' + detail[11] + '">' +
            '<div class="form-floating mb-3">' +
            '<select class="form-select" id="use_status">' +
            '<option value="">---</option>' +
            '<option value="new"'
        if (detail[10] === 'new') {
            $inner_html += 'selected'
        }
        $inner_html += '">new</option>' +
            '<option value="used"'
        if (detail[10] === 'used') {
            $inner_html += 'selected'
        }
        $inner_html += '">used</option>' +
            '<option value="as new"'
        if (detail[10] === 'as new') {
            $inner_html += 'selected'
        }
        $inner_html += '">as new</option>' +
            '</select>' +
            '<label for="use_status">Status:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="parcode_select">' +
            '<select class="form-select" id="partcode" size="5" aria-label="size 5 select partcode"></select>' +
            '<label for="partcode">Partcode:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<button class="btn btn-success save" value="' + detail[0] + '">save</button>' +
            '</div>' +
            '</form>'

        $('#detail_item').html($inner_html)
    }
}

$(document).on('keyup', '#parcode_select', function () {
    val = $(this).val().toLowerCase()
    console.log(val)
    if (val.length > 2) {
        spartcode = partcodes.filter(x => x[1].replace(/\(/g, '[').replace(/\)/g, ']').toLowerCase().indexOf(val) > -1)
        $html = ''
        spartcode.forEach(item => {
            $html += '<option value="' + item[0] + '">' + item[1] + '</option>'
        })
        $('#partcode').append().html($html)
    } else {
        spartcode = partcodes
    }
})

$(document).on('click', '.save', function (event) {
    $(this).addClass('disabled')
    did = $(this).val()
    spr_id = $('#spr_id').val()
    detail_name = $('#detail_name').val()
    description = $('#description').val()
    seo = $('#seo').val()
    base_img = $('#base_img').val()
    detail_price = $('#detail_price').val()
    vendor = $('#vendor_price').val()
    use_status = $('#use_status').val()
    partcode = $('#partcode').val()
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.stopPropagation();
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/dashboard/details',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "action": 'save',
            "did": did,
            "spr_id": spr_id,
            "detail_name": detail_name,
            "description": description,
            "base_img": base_img,
            "seo": seo,
            "detail_price": detail_price,
            "vendor": vendor,
            "use_status": use_status,
            "partcode": partcode,
            "price_id": $('#price_id').val()
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            $('.save').removeClass('disabled')
        }
    });
})

detail_show();