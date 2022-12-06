
$(document).ready(function () {
    $('#snippet-button').on('click', function () {
        var $snippet_textarea = $('#message-textarea');
        var message = $snippet_textarea.val();
        if (message.trim() !== '') {
            $snippet_textarea.val('');

            document.getElementById("i-box-about").innerHTML=message;


        }
    });
    $(".aaatete").off("click").on("click",function(){
        var x = document.getElementById("edit1")
        if(x.style.display=="block"){
            x.style.display="none";
        }else{
            x.style.display="block";
        };
    });

    $(".hsbtn").off("click").on("click",function(){
        if ($(this).parent().parent().hasClass("post")){
            $(this).parent().parent().removeClass("post")
            $(this).parent().parent().addClass("post-show")
        }else{
            $(this).parent().parent().addClass("post")
            $(this).parent().parent().removeClass("post-show")
        }

    });


 });