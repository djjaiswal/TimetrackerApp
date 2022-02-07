function enableform(){
    document.getElementsByClassName("data-adding-form")[0].classList.remove("hide");
    document.getElementsByClassName("add-new")[0].classList.add("hide")
}


function closeform(){
event.preventDefault()
document.getElementsByClassName("data-adding-form")[0].classList.add("hide");
document.getElementsByClassName("add-new")[0].classList.remove("hide")
}
function close_flash(){
     document.getElementsByClassName("alert")[0].classList.add("hide")
}


jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});
