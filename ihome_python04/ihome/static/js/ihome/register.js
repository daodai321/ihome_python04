function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 保存图片验证码编号
var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}


function generateImageCode() {
    // 形成图片验证码的后端地址， 设置到页面中，让浏览请求验证码图片
    // 1. 生成图片验证码编号
    imageCodeId = generateUUID();
    // 是指图片url
    var url = "/api/v1.0/image_codes/" + imageCodeId;
    $(".image-code img").attr("src", url);
}

function sendSMSCode(){
    $(".phonecode-a").removeAttr("onclick")
    // 获取填写的图片验证码,手机号
    var mobile = $("#mobile").val();
    // 判断手机号,图片验证码的完整性
    if (!mobile){
        $("#mobile-err span").html("请填写手机号");
        $("#mobile-err").show();
        $(".phonecode-a").attr(onclick,"sendSMSCode();");
        return
    }
    var image_code = $("#imagecode").val();
    if (!image_code){
        $("image-code-err span").html("请填写图片验证码")
        $("image-code-err").show()
        $(".phonecode-a").attr(onclick,"sendSMSCode();")
        return
    }
    var requ_data={
        "image_code":image_code,
        "image_code_id":imageCodeId      
    }
    $.get("/api/v1.0/sms_codes/"+mobile,requ_data,function(resp){
        if (resp.errno == "0"){
            // 发送成功
            var num = 60;
            var timer = setInterval(function () {
                if (num >= 1){
                    $(".phonecode-a").html(num+"秒");
                    num -= 1
                }else{
                    $(".phonecode-a").html("获取验证码");
                    $(".phonecode-a").attr("onclick","sendSMSCode();");
                    clearInterval(timer);
                }
            },1000,60)
            
        }else{
            alert(resp.errmsg)
            $(".phonecode-a").attr("onclick","sendSMSCode();")
        }
    })
}


$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });

    $(".form-register").submit(function (e) {
        e.preventDefault();
        //mobile, imagecode, phonecode, password, password2
        var mobile = $("#mobile").val();
        if (!mobile){
            $("#mobile-err span").html("请填写手机号");
            $("#mobile-err").show();
            return;
        }
        var imagecode = $("#imagecode").val();
        if(!imagecode){
            $("#image-code-err span").html("请填写图片验证码");
            $("#image-code-err").show();
            return;
        }
        var phonecode = $("#phonecode").val();
        if(!phonecode){
            $("#phone-code-err span").html("请填写手机验证码")
            $("#phone-code-err").show();
            return;
        }
        var passwd = $("#password").val();
        if (!passwd){
            $("#password-err span").html("请填写密码");
            $("#password-err").show();
            return;
        }
        var passwd2 = $("#password2").val();
        if (!passwd2){
            $("#password2-err span").html("请再次确认密码");
            $("#password2-err").show();
            return;
        }

        if (passwd != passwd2){
            $("#password2-err span").html("两次密码不一致,请重新填写");

        }
        var req_dict ={
            "mobile":mobile,
            "sms_code":phonecode,
            "password":passwd,
            "password2":passwd2
        };
        var req_json = JSON.stringify(req_dict);
        $.ajax({
            url:"/api/v1.0/users",
            type:"post",
            data:req_json,
            contentType:"application/json",
            dataType:"json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success:function (resp) {
                if (resp.errno == "0"){
                    location.href="index.html";
                }
                else {
                    alert(resp.errmsg);
                }
            }

        })

    });





    // $(".form-register").submit(function(e){
    //     e.preventDefault();
    //     mobile = $("#mobile").val();
    //     phoneCode = $("#phonecode").val();
    //     passwd = $("#password").val();
    //     passwd2 = $("#password2").val();
    //     if (!mobile) {
    //         $("#mobile-err span").html("请填写正确的手机号！");
    //         $("#mobile-err").show();
    //         return;
    //     }
    //     if (!phoneCode) {
    //         $("#phone-code-err span").html("请填写短信验证码！");
    //         $("#phone-code-err").show();
    //         return;
    //     }
    //     if (!passwd) {
    //         $("#password-err span").html("请填写密码!");
    //         $("#password-err").show();
    //         return;
    //     }
    //     if (passwd != passwd2) {
    //         $("#password2-err span").html("两次密码不一致!");
    //         $("#password2-err").show();
    //         return;
    //     }
    // });



})