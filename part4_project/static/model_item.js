$('.nav-link').click(function (e) {
    e.preventDefault()
    $area = $(this).attr('aria-controls')
    $('.nav-link').removeClass('active')
    $('.tab-pane').removeClass('active')
    $('#'+$area).addClass('active')
    $(this).addClass('active')
    return false;
})