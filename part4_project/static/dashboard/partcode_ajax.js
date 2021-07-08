// String to json
function toJSON(item) {
    item = item.replace('True', '"True"').replace(/&#x27;/g, "'").replace(/'/g, '"').replace(/\\/g, '/').replace(/\(/g, '[').replace(/\)/g, ']').replace(/None/g, '""').replace(/\n/g, '').replace(/Decimal/g, '')
    return JSON.parse(item)
}

model_id = null
module_id = null

function detail_show() {
    if (partcode.length > 0) {
        brands = toJSON(brands)
        partcode = toJSON(partcode)[0]
        models = toJSON(models)
        modules = toJSON(modules)
        linking = toJSON(linking)
        $linking = '<hr>'
        linking.forEach(lnk => {
            $linking += '<p>' + models[parseInt(lnk[1])-1][1] + ' / ' + modules[parseInt(lnk[2])-1][1] + '' +
                '<button class="btn btn-danger btn-link remove" value="' + partcode[0] +
                '"area-id="'+models[parseInt(lnk[1])-1][0]+'" ' +
                'id="'+modules[parseInt(lnk[2])-1][0]+'"><span class="material-icons">remove</span></button></p>'
        })
        $inner_html = '<h4><small>partcode: </small>' + partcode[1] + '</h4>' +
            '<form class="form-floating" type="POST"><div class="row"><div class="col-5">\n' +
            '<div class="form-floating mb-3">\n' +
                '<input type="text" class="form-control" id="partcode_image" placeholder="" value="' + partcode[2] + '">\n' +
                '<label for="partcode_image">Image:</label></div>\n' +
            '<div class="form-floating mb-3">\n' +
                '<input type="text" class="form-control" id="partcode_article" placeholder="" value="' + partcode[3] + '">\n' +
                '<label for="partcode_article">Article:</label></div>' +
            '<div class="form-floating mb-3">\n' +
                '<input type="text" class="form-control" id="partcode_desc" value="' + partcode[4] + '">\n' +
                '<label for="partcode_desc">Description:</label></div>' +
            '<input type="hidden" id="dictionary_partcode_id" value="'+ partcode[5] +'"></div>'+
            '<div class="col-7"><h4>Добавить модель/модуль</h4> <div class="row">' +
                '<div class="col-12"><div class="form-floating mb-3">\n' +
                    '<div class="input-group">' +
                    '<input type="text" class="form-control" id="new_model" value="">' +
                    '<span class="input-group-text" id="new_model_name"></span>\n' +
                    '</div></div>' +
                '<div id="list_model"></div></div>' +
                '<div class="col-12"><div class="form-floating mb-3">\n' +
                    '<div class="input-group">' +
                    '<input type="text" class="form-control" id="new_module" value="">\n' +
                    '<span class="input-group-text" id="new_module_name"></span>\n' +
                    '</div></div>' +
                '<div id="list_module"></div></div>' +
            '</div></div>' +

            '<div class="col-12">' +
            '<div class="form-check form-switch bg-light">\n' +
                '<input type="checkbox" class="form-check-input" id="change_for_all">\n' +
                '<label class="form-check-label" for="change_for_all">Поменять для всех:</label></div>' +
            '<div class="form-floating mb-3">\n' +
                '<input type="text" class="form-control" id="partcode_name_en" value="' + partcode[8] + '">\n' +
                '<label for="partcode_name_en">Name en:</label></div>' +
            '<div class="form-floating mb-3">\n' +
                '<input type="text" class="form-control" id="partcode_name_ru" value="' + partcode[9] + '">\n' +
                '<label for="partcode_name_ru">Name ru:</label></div>' +
            '<div class="form-floating mb-3">\n' +
                '<input type="text" class="form-control" id="partcode_desc_en" value="' + partcode[11] + '">\n' +
                '<label for="partcode_desc_en">Description en:</label></div>' +
            '<div class="form-floating mb-3">\n' +
                '<input type="text" class="form-control" id="partcode_desc_ru" value="' + partcode[12] + '">\n' +
                '<label for="partcode_desc_ru">Description ru:</label></div>' +
            '<button class="btn btn-success save" value="' + partcode[0] + '">save</button></div>' +
            '</div></form>'
        $inner_html += $linking
        $('#partcode_item').html($inner_html)

        $('#new_model').keyup(function () {
            let val = $(this).val().toLowerCase();
            if (val.length > 2) {
                smodels = models.filter(x => x[1].toLowerCase().indexOf(val) > -1)
                $html = ''
                smodels.forEach(item => {
                    $html += '<button type="button" class="btn btn-link btn_show_model" value="' + item[1] + '" ' +
                        'model_id="' + item[0] + '">' + item[1] + '</button>'
                })
                $('#list_model').append().html($html)
            } else {
                smodels = models
            }
        })
        $(document).on('click', '.btn_show_model', function (event) {
            model_id = $(this).attr('model_id');
            model = $(this).val();
            $('#new_model').val('')
            $('#new_model_name').html(model)
            $('#list_model').html('')
        })

        $('#new_module').keyup(function () {
            let val = $(this).val().toLowerCase();
            if (val.length > 2) {
                smodels = modules.filter(x => x[1].toLowerCase().indexOf(val) > -1)
                $html = ''
                smodels.forEach(item => {
                    $html += '<button type="button" class="btn btn-link btn_show_module" value="' + item[1] + '" ' +
                        'module_id="' + item[0] + '">' + item[1] + '</button>'
                })
                $('#list_module').append().html($html)
            } else {
                smodels = modules
            }
        })
        $(document).on('click', '.btn_show_module', function (event) {
            module_id = $(this).attr('module_id');
            module = $(this).val();
            $('#new_module').val('')
            $('#new_module_name').html(module)
            $('#list_module').html('')
        })
    }
}

$(document).on('click', '.remove', function (event) {
    $('.save').addClass('disabled')
    pid = $(this).val()
    model_id = $(this).attr('area-id')
    module_id = $(this).attr('id')
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.stopPropagation();
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/dashboard/partcodes',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            "action": 'remove',
            "pid": pid,
            'model_id': model_id,
            'module_id': module_id,
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            $('.save').removeClass('disabled')
        }
    });
})

$(document).on('click', '.save', function (event) {
    $(this).addClass('disabled')
    pid = $(this).val()
    dictionary_partcode_id = $('#dictionary_partcode_id').val()
    partcode_name_en = $('#partcode_name_en').val()
    partcode_desc_en = $('#partcode_desc_en').val()
    partcode_name_ru = $('#partcode_name_ru').val()
    partcode_desc = $('#partcode_desc').val()
    partcode_desc_ru = $('#partcode_desc_ru').val()
    partcode_image = $('#partcode_image').val()
    partcode_article = $('#partcode_article').val()
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
            "partcode_image": partcode_image,
            "partcode_article": partcode_article,
            "partcode_desc": partcode_desc,
            'model_id': model_id,
            'module_id': module_id,
            "for_all": $('#change_for_all')[0].checked,
            'dictionary_partcode_id': dictionary_partcode_id,
            'partcode_name_en': partcode_name_en,
            'partcode_name_ru': partcode_name_ru,
            "partcode_desc_en": partcode_desc_en,
            "partcode_desc_ru": partcode_desc_ru,
        },
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        success: function (data) {
            $("#detail_item").html('').append(data);
            $('.save').removeClass('disabled')
        }
    });
})

detail_show();