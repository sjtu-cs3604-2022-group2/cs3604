
function show(){
    var btnobj=document.getElementById("btn1");
    var navobj=document.getElementById("nav1-1");
    var navobj2=document.getElementById("btn2");
    var navobj3=document.getElementById("btn3");
    var divobj1=document.getElementById("show1");
    var divobj2=document.getElementById("show2");
    var divobj3=document.getElementById("show3");
    var divobj4=document.getElementById("show4");
    if(btnobj.value=="显示"){


    }else{
        divobj1.style.display="none";
        divobj2.style.display="block";
        divobj3.style.display="none";
        divobj4.style.display="none";
        btnobj.value="显示";
        navobj.value="隐藏";
        navobj2.value="隐藏";
        navobj3.value="隐藏";
        $("#p-tabs-m #nav1-1").removeClass("active");
        $("#p-tabs-m #btn1").addClass("active");
        $("#p-tabs-m #btn2").removeClass("active");
        $("#p-tabs-m #btn3").removeClass("active");
    }
}
function show1(){
    var btnobj=document.getElementById("nav1-1");
    var navobj=document.getElementById("btn1");
    var navobj2=document.getElementById("btn2");
    var navobj3=document.getElementById("btn3");
    var divobj1=document.getElementById("show1");
    var divobj2=document.getElementById("show2");
    var divobj3=document.getElementById("show3");
    var divobj4=document.getElementById("show4");
    if(btnobj.value=="显示"){


    }else{
        divobj2.style.display="none";
        divobj1.style.display="block";
        divobj3.style.display="none";
        divobj4.style.display="none";
        btnobj.value="显示";
        navobj.value="隐藏";
        navobj2.value="隐藏";
        navobj3.value="隐藏";
        $("#p-tabs-m #nav1-1").addClass("active");
        $("#p-tabs-m #btn1").removeClass("active");
        $("#p-tabs-m #btn2").removeClass("active");
        $("#p-tabs-m #btn3").removeClass("active");
    }
}

function show2(){
    var navobj2=document.getElementById("nav1-1");
    var navobj=document.getElementById("btn1");
    var btnobj=document.getElementById("btn2");
    var navobj3=document.getElementById("btn3");
    var divobj1=document.getElementById("show1");
    var divobj2=document.getElementById("show2");
    var divobj3=document.getElementById("show3");
    var divobj4=document.getElementById("show4");
    if(btnobj.value=="显示"){


    }else{
        divobj1.style.display="none";
        divobj2.style.display="none";
        divobj3.style.display="block";
        divobj4.style.display="none";
        btnobj.value="显示";
        navobj.value="隐藏";
        navobj2.value="隐藏";
        navobj3.value="隐藏";
        $("#p-tabs-m #btn2").addClass("active");
        $("#p-tabs-m #btn1").removeClass("active");
        $("#p-tabs-m #nav1-1").removeClass("active");
        $("#p-tabs-m #btn3").removeClass("active");
    }
}
function show3(){
    var navobj2=document.getElementById("nav1-1");
    var navobj=document.getElementById("btn1");
    var navobj3=document.getElementById("btn2");
    var btnobj=document.getElementById("btn3");
    var divobj1=document.getElementById("show1");
    var divobj2=document.getElementById("show2");
    var divobj3=document.getElementById("show3");
    var divobj4=document.getElementById("show4");
    if(btnobj.value=="显示"){


    }else{
        divobj1.style.display="none";
        divobj2.style.display="none";
        divobj4.style.display="block";
        divobj3.style.display="none";
        btnobj.value="显示";
        navobj.value="隐藏";
        navobj2.value="隐藏";
        navobj3.value="隐藏";
        $("#p-tabs-m #btn3").addClass("active");
        $("#p-tabs-m #btn1").removeClass("active");
        $("#p-tabs-m #nav1-1").removeClass("active");
        $("#p-tabs-m #btn2").removeClass("active");
    }
}



 // 函数封装 获取指定类名下的所有指定元素
 const getElementsByLocalNameOfClassName = function (className, elementName) {
    let grandfather = document.getElementsByClassName(`${className}`);//获取所有类名为aCuteName的元素
    let children = []//用来接收要获取的数据
    for (let i of grandfather) {
        let father = i.childNodes;//获取每个类名为aCuteName元素的子元素合集
        for (let j in father) {
            if (father[j].localName === `${elementName}`)//通过localName获取input元素合集
                children.push(father[j]);//将所有input保存在一个数组中
        }
    }
    return children;
}

function ChooseFavor(aTag){
    var text = aTag.innerText;
    document.getElementById("favor-choose").innerText=text;
    var num_order = parseInt(aTag.getAttribute("value"));
    let favors_all = getElementsByLocalNameOfClassName('favor-all','ul');
    setNone();
    favors_all[num_order].setAttribute('style','display:block;width:100%;');

}
function setNone(){
    let inputsOfaCuteName = getElementsByLocalNameOfClassName('favor-all','ul');
    for (let i of inputsOfaCuteName) {
        i.setAttribute('style','display:none');
    }

}
function showFavor(favor_table){
    setNone();
    favor_table.setAttribute('style','display:block');
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

