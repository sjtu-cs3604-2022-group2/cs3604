var date = new Date();
document.getElementById("curr-year").innerHTML = date.getFullYear();
function show(){
    var btnobj=document.getElementById("btn1");
    var navobj=document.getElementById("nav1-1");
    var divobj1=document.getElementById("show1");
    var divobj2=document.getElementById("show2");

    if(btnobj.value=="显示"){


    }else{
        divobj1.style.display="none";
        divobj2.style.display="block";
        btnobj.value="显示";
        navobj.value="隐藏";
        $("#p-tabs-m #nav1-1").removeClass("active");
        $("#p-tabs-m #btn1").addClass("active");
    }
}
function show1(){
    var btnobj=document.getElementById("nav1-1");
    var navobj=document.getElementById("btn1");
    var divobj1=document.getElementById("show1");
    var divobj2=document.getElementById("show2");

    if(btnobj.value=="显示"){


    }else{
        divobj2.style.display="none";
        divobj1.style.display="block";
        btnobj.value="显示";
        navobj.value="隐藏";
        $("#p-tabs-m #nav1-1").addClass("active");
        $("#p-tabs-m #btn1").removeClass("active");
    }
}