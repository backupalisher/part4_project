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
    })
})