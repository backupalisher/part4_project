$(document).ready(function(){
    var inProgress = false;
    var startFrom = 10;
    $(window).scroll(function() {
        if($(window).scrollTop() + $(window).height() >= $(document).height() - 200 && !inProgress) {
            inProgress = true;
            console.log($(window).scrollTop())
            console.log($(window).height())
            console.log($(document).height())
            setTimeout(()=>{startFrom += 10;}, 2000)
            inProgress = false;
        }
    });

    //Scrolling in parts tab
    $('#parts-tab').click(function () {
        setTimeout(()=>{
            partsHeight = $('#parts').height()
            if (partsHeight > 360) {
                $('.model-opts').css('max-height', partsHeight)
           } else {
                console.log(partsHeight)
                $('.model-opts').css('max-height', 360)
            }
        }, 10)
    });

    //Filter by model name
    function filter_search(e) {
        elements = $('.card-model')
        elements.each(function() {
            //console.log($( this ).parent())
            $( this ).parent()[0].style.display = 'none'
            e_str = ($( this )[0].innerHTML).toString()
            if (e_str.toLowerCase().indexOf(e.toLowerCase()) >= 0) {
                 $( this ).parent()[0].style.display = 'block'
            }
        })
    }
    $('#filter_search').keyup(function (e) {
        val = $(this).val()
        //if(e.which == 13) {
        if(val.length > 1) {
            console.log(val)
            filter_search(val)
        } else {
            filter_search('')
        }
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
})