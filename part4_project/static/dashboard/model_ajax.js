// String to json
function toJSON(item) {
    item = item.replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\\/g, '/').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    return JSON.parse(item)
}

function model_show() {
    if (model.length > 0) {
        moduls = toJSON(moduls)
        brands = toJSON(brands)
        model = toJSON(model)
        vendors = toJSON(vendors)
        console.log(vendors)
        $inner_html = '<form class="form-floating" id="model_save">\n' +
            '<div class="form-floating mb-3">\n' +
            '<input type="text" class="form-control" id="model_name' + model[0][1] + '" value="' + model[0][2] + '">\n' +
            '<label for="model_name">Model:</label></div>\n' +
            '<div class="form-floating mb-3">\n' +
            '<input type="text" class="form-control" id="model_main_image" placeholder="" value="' + model[0][4] + '">\n' +
            '<label for="model_main_image">Main image:</label></div>\n' +
            '<div class="form-floating mb-3">\n' +
            '<input type="text" class="form-control" id="model_image" placeholder="" value="' + model[0][5] + '">\n' +
            '<label for="model_image">Image:</label></div>\n' +
            '<div class="form-floating mb-3">' +
            '<select class="form-select" id="model_brand_name">'
                for (let i = 0; i < brands.length; i++) {
                    $inner_html += '<option value="' + brands[i][0] + '"'
                    if (model[0][6] === brands[i][1]) {
                        $inner_html += ' selected>'
                    }
                    $inner_html += brands[i][1] + '</option>'
                }
                $inner_html += '</select>' +
            '<label for="model_brand_name">Brand:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<select class="form-select" id="vendor_price">' +
                    '<option value="'+model[0][8]+'">---</option>'
                for (let i = 0; i < vendors.length; i++) {
                    $inner_html += '<option value="' + vendors[i][0] + '"'
                    if (model[0][8] === vendors[i][0]) {
                        $inner_html += ' selected>'
                    } else {
                        $inner_html += ' >'
                    }
                    $inner_html += vendors[i][1] + '</option>'
                }
                $inner_html += '</select>' +
            '<label for="vendor_price">Vendor:</label></div>' +
            '<div class="form-floating mb-3">' +
            '<input type="text" class="form-control" id="model_price" value="' + model[0][7] + '">' +
            '<label for="model_price">Price:</label></div>' +
            '<input type="hidden" id="price_id" value="'+model[0][9]+'">'
        for (let i = 0; i < moduls.length; i++) {
            $inner_html += '<p><a class="btn btn-link" type="button" data-bs-toggle="collapse" ' +
                'aria-expanded="false" data-bs-target="#module' + moduls[i][1] + '" ' +
                'aria-controls="module' + moduls[i][1] + '">' + moduls[i][4] + '</a></p>' +
                '<div class="collapse mb-3" id="module' + moduls[i][1] + '"><div class="card card-body">' +
                '<div class="form-floating mb-3">' +
                '<input type="text" class="form-control" id="module' + moduls[i][1] + '" value="' + moduls[i][4] + '">' +
                '<label for="module' + moduls[i][1] + '">Module:</label></div>' +
                '<div class="form-floating mb-3">' +
                '<input type="text" class="form-control" id="m_description' + moduls[i][2] + '" value="' + moduls[i][5] + '">' +
                '<label for="m_description' + moduls[i][1] + '">Module description:</label></div>' +
                '<div class="form-floating mb-3">' +
                '<input type="text" class="form-control" id="m_scheme_picture' + moduls[i][2] + '" value="' + moduls[i][6] + '">' +
                '<label for="m_scheme_picture' + moduls[i][1] + '">Module scheme_picture:</label></div>' +
                '<div class="form-floating mb-3">' +
                '<input type="text" class="form-control" id="m_name_ru' + moduls[i][2] + '" value="' + moduls[i][7] + '">' +
                '<label for="m_name_ru' + moduls[i][1] + '">Module name_ru:</label></div>' +
                '<div class="form-floating mb-3">' +
                '<input type="text" class="form-control" id="m_image' + moduls[i][2] + '" value="' + moduls[i][9] + '">' +
                '<label for="m_image' + moduls[i][2] + '">Module image:</label></div>' +
                '</div></div>'
        }
        $inner_html += '<div class="form-floating mb-3">' +
            '<button class="btn btn-success save" id="' + model[0][1] + '">save</button></div></form>'

        $('#model_detail').html($inner_html)
    }
}

$(document).on('click', '.save', function (event) {
    // $(this).addClass('disabled')
    limit = 20
    offset = 0
    $data = []
    console.log(document.forms[0].elements.length-1)
    for (let i = 0; i < document.forms[0].elements.length-1; i++) {
        val = document.forms[0].elements[i].value.toString()
        id = document.forms[0].elements[i].id.toString()
        $data.push({id, val})
    }
    console.log($data)
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.stopPropagation();
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/dashboard/models',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "action": 'save_model',
            "data": JSON.stringify($data),
            "limit": limit,
            "offset": offset,
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            console.log('success')
            $(document.getElementsByClassName('.save')).removeClass('disabled')
        }
    });
})

model_show();