if ($('.profile-form').length > 0) {
    $('.profile-form').keyup(function () {
        if ($('#repassword').val() === $('#password').val() && $('#repassword').val().length === 0) {
            $('.profile-form button').prop('disabled', false);
            $('.profile-form button').removeClass('disabled')
            $('.profile-form .warning').removeClass('active')
        }
    })
    $('#repassword').keyup(function () {
        if ($('#repassword').val() === $('#password').val() && $('#repassword').val().length > 5) {
            $('.profile-form button').prop('disabled', false);
            $('.profile-form button').removeClass('disabled')
            $('.profile-form .warning').removeClass('active')
        } else {
            $('.profile-form button').addClass('disabled')
            $('.profile-form .warning').addClass('active')
        }
    })
}