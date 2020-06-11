$(document).ready(function () {
    $pathname = window.location.pathname;
    //Wait for element exist
    var waitForEl = function (selector, callback) {
        if (jQuery(selector).length) {
            callback();
        } else {
            setTimeout(function () {
                waitForEl(selector, callback);
            }, 100);
        }
    };

    var inProgress = false;
    var startFrom = 10;
    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 200 && !inProgress) {
            inProgress = true;
            setTimeout(() => {
                startFrom += 10;
            }, 2000)
            inProgress = false;
        }
    });

    //Scrollbar
    jQuery(document).ready(function () {
        jQuery('.scrollbar-macosx').scrollbar();
    });

    //Scrolling in parts tab
    // waitForEl('#parts', function () {
    //     partsHeight = $('#parts').height()
    //     if (partsHeight > 360) {
    //         $('.model-opts').css('max-height', partsHeight)
    //    } else {
    //         $('.model-opts').css('max-height', 360)
    //    }
    // })
    // $('#parts-tab').click(function () {
    //     setTimeout(()=>{
    //         partsHeight = $('#parts').height()
    //         if (partsHeight > 360) {
    //             $('.model-opts').css('max-height', partsHeight)
    //        } else {
    //             $('.model-opts').css('max-height', 360)
    //        }
    //     }, 10)
    // });

    //Filter by model name
    function filter_search(e) {
        elements = $('.card-model-item')
        elements.each(function () {
            //console.log($( this ).parent())
            $(this).parent()[0].style.display = 'none'
            e_str = ($(this)[0].innerHTML).toString()
            if (e_str.toLowerCase().indexOf(e.toLowerCase()) >= 0) {
                $(this).parent()[0].style.display = 'block'
            }
        })
    }

    $('#filter_search').keyup(function (e) {
        val = $(this).val()
        //if(e.which == 13) {
        if (val.length > 1) {
            filter_search(val)
        } else {
            filter_search('')
        }
    })
    $('#filter_search_clear').click(function () {
        $('#filter_search').val('')
        filter_search('')
    })

    //Toggle themes
    $('#toggle-theme').click(function () {
        console.log('change')
        if ($('#body').hasClass('dark-theme')) {
            $('#body').removeClass('dark-theme')
            $('#body').addClass('light-theme')
        } else {
            $('#body').removeClass('light-theme')
            $('#body').addClass('dark-theme')
        }
    })

    //Search position and vals save
    if ($pathname.indexOf('search') > 0) {
        vals = getUrlVars($pathname)
        if (vals.length > 0) {
            localStorage.setItem('variant', vals['v'])
            localStorage.setItem('sval', decodeURIComponent(vals['s']))
        }
        if (localStorage.getItem('variant') && localStorage.getItem('sval')) {
            $v = localStorage.getItem('variant')
            console.log(localStorage.getItem('sval'))
            $s = localStorage.getItem('sval').replace(/\+/g, ' ')
            $('#search_main .custom-select').val($v)
            $('#search_main input').val($s)
        }
    }

    //Save selected filter options
    if ($pathname.indexOf('brand') > 0) {
        // $("form").submit(function (event) {
        //         // Stop form from submitting normally
        //         event.preventDefault();
        //
        //         /* Serialize the submitted form control values to be sent to the web server with the request */
        //         var formValues = $(this).serialize();
        //         console.log(formValues)
        //     }
        // )
    }
})

function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}