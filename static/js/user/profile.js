var date = new Date();
document.getElementById("curr-year").innerHTML = date.getFullYear();
function show(){
    var btnobj=document.getElementById("btn1");
    var navobj=document.getElementById("nav1-1");
    var navobj2=document.getElementById("btn2");
    var divobj1=document.getElementById("show1");
    var divobj2=document.getElementById("show2");
    var divobj3=document.getElementById("show3");

    if(btnobj.value=="显示"){


    }else{
        divobj1.style.display="none";
        divobj2.style.display="block";
        divobj3.style.display="none";
        btnobj.value="显示";
        navobj.value="隐藏";
        navobj2.value="隐藏";
        $("#p-tabs-m #nav1-1").removeClass("active");
        $("#p-tabs-m #btn1").addClass("active");
        $("#p-tabs-m #btn2").removeClass("active");
    }
}
function show1(){
    var btnobj=document.getElementById("nav1-1");
    var navobj=document.getElementById("btn1");
    var navobj2=document.getElementById("btn2");
    var divobj1=document.getElementById("show1");
    var divobj2=document.getElementById("show2");
    var divobj3=document.getElementById("show3");
    if(btnobj.value=="显示"){


    }else{
        divobj2.style.display="none";
        divobj1.style.display="block";
        divobj3.style.display="none";
        btnobj.value="显示";
        navobj.value="隐藏";
        navobj2.value="隐藏";
        $("#p-tabs-m #nav1-1").addClass("active");
        $("#p-tabs-m #btn1").removeClass("active");
        $("#p-tabs-m #btn2").removeClass("active");
    }
}

function show2(){
    var navobj2=document.getElementById("nav1-1");
    var navobj=document.getElementById("btn1");
    var btnobj=document.getElementById("btn2");
    var divobj1=document.getElementById("show1");
    var divobj2=document.getElementById("show2");
    var divobj3=document.getElementById("show3");
    if(btnobj.value=="显示"){


    }else{
        divobj1.style.display="none";
        divobj2.style.display="none";
        divobj3.style.display="block";
        btnobj.value="显示";
        navobj.value="隐藏";
        navobj2.value="隐藏";
        $("#p-tabs-m #btn2").addClass("active");
        $("#p-tabs-m #btn1").removeClass("active");
        $("#p-tabs-m #nav1-1").removeClass("active");
    }
}
$(document).ready(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });





})
