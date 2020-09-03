if ($errors.length > 0) {
    $errors = $errors.replace(/\(/g, '[').replace(/\)/g, ']')
        .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
        .replace(/&#x27;/g, "'").replace(/&quot;/g, '"')
        .replace(/'/g, '"').replace(/""/g, '"')
        .replace(/"s/g, '\'s').replace(/"t/g, '\'t')
        .replace(/None/g, '""')
    console.log($errors)
    $errors = JSON.parse($errors)
    $errors_all = $errors
    show_cartridges($errors_all)

}

function search_errors(s) {
    $errors_all = []
    for (let i = 0; i < $errors.length; i++) {
        console.log($errors[i])
        if ($errors[i][2].toLowerCase().indexOf(s.toLowerCase()) > -1
            || $errors[i][3].toLowerCase().indexOf(s.toLowerCase()) > -1
            || $errors[i][4].toLowerCase().indexOf(s.toLowerCase()) > -1
            || $errors[i][5].toLowerCase().indexOf(s.toLowerCase()) > -1) {
            $errors_all.push($errors[i])
        }
    }
    show_errors($errors_all)
}

$('#errors_search').keyup(function () {
    let sval = $(this).val()
    if (sval.length > 1) {
        $('#accordion').html('')
        search_errors(sval)
    } else {
        $errors_all = $errors
        $('#accordion').html('')
        show_errors($errors_all)
    }
})

function show_errors(errors) {
    if (errors.length > 0) {
        for (let i = 0; i < errors.length; i++) {
            $html = '<div class="card error-list"> <div class="card-header" id="headingOne"> <h5 class="mb-0"> ' +
                '        <button class="btn btn-link" data-toggle="collapse" data-target="#collapse' + i + '" ' +
                '        aria-expanded="false" aria-controls="collapseOne"> ' +
                '        <span class="errorcode">' + errors[i][2] + '</span> </button> </h5> </div>' +
                '    <div id="collapse' + i + '" class="collapse" aria-labelledby="headingOne" data-parent="#accordion"> ' +
                '           <div class="card-body"> '
            if (errors[i][3]) {
                $html += '<p><span class="display">Display:</span> '+ errors[i][3] +'</p> {% endif %}'
            }
            if (errors[i][4]) {
                $html += '<p><span class="description">Description:</span> '+ errors[i][4] +'</p> {% endif %}'
            }
            if (errors[i][5]) {
                $html += '<p><span class="causes">Causes:</span> '+ errors[i][5] +'</p> {% endif %}'
            }
            if (errors[i][6]) {
                $html += '<p><span class="remedy">Remedy:</span> '+ errors[i][6] +'</p> {% endif %}'
            }
            $html += ' </div> </div> </div>'
        }
    }
}
