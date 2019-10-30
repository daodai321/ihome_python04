function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(document).ready(function(){
    $.get("/api/v1.0/users/auth",function(resp){
        if (resp.errno=="4101"){
            location.href="/login.html"
        }else if(resp.errno=="0"){
            if (resp.data.user.real_name&&resp.data.user.id_card){
                $("#real-name").val(resp.data.user.real_name);
                $("#id-card").val(resp.data.user.id_card);
                $("#real-name").prop("distabled",true);
                $("#id-card").prop("distabled",true);
                $("#form-auth>input[type=submit]").hide()
            }
        }else {
            alert(resp.errmsg)
        }
    },"json");

    $("#form-auth").submit(function (e) {
        e.preventDefault();
        var real_name = $("#real-name").val();
        var id_card = $("#id-card").val();
        var data = {
            "real_name":real_name,
            "id_card":id_card
        };
        var data_json = JSON.stringify(data);

        $.ajax({
            url:"/api/v1.0/users/auth",
            type:"post",
            contentType:"application/json",
            dataType:"json",
            data:data_json,
            headers:{
                "X-CSRF-Token":getCookie("csrf_token")
            },
            success:function (resp) {
                if(resp.errno=="4101"){
                    location.href="/login.html"
                }else if (resp.errno=="0"){
                    $(".error-msg").hide();
                    showSuccessMsg();
                    $("#form-auth input[type=submit]").hide();
                    $("#id-card").prop("disabled", true);
                    $("#real-name").prop("disabled", true);
                }else{
                    alert(resp.errmsg)
                }
            }
        })
    })


})





