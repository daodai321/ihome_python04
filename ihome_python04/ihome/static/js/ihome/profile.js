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

$(document).ready(function () {
    $("#form-avatar").submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url:"api/v1.0/users/avatar",
            type:"post",
            dataType:"json",
            headers:{
              "X-CSRFToken": getCookie("csrf_token")
            },
            success:function (resp) {
                if (resp.errno == "0"){
                    var avatarUrl = resp.data.avatar_url;
                    $("#user-avatar").attr("src",avatarUrl)
                }else{
                    alert(resp.errmsg)
                }
            }
        })
    })

    $("#form-name").submit(function(e){
        e.preventDefault();
        var user_name = $("#user-name").val();
        if (!user_name){
            alert("请填写用户名")
        }
        $.ajax({
            url:"user/auth",
            type:"put",
            contentType:"application/json",
            data:JSON.stringify(user_name),
            dataType:"json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success:function (resp) {
                if (resp.error=="0"){
                    $(".error-msg").hide();
                    showSuccessMsg()
                }else if(resp.error=="4001"){
                    $(".error-msg").show()
                }else if(resp.error=="4101"){
                    location.href = "login/html"
                }
            }
        })


    })


})


