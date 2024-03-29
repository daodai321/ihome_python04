function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function logout() {
    $.ajax({
        url:"/api/v1.0/session",
        type:"delete",
        headers:{
            "X-CSRFToken":getCookie("csrf_token")
        },
        dataType:"json",
        success: function(resp){
            if (resp.errno=="0"){
                 location.href = "/index.html";
            }
        }
    })
}

$(document).ready(function(){
    $.get("/api/v1.0/user",function(resp){
        if(resp.errno=="4101"){
            alert("用户未登录");
            location.href("/login/html")
        }else if(resp.errno=="0"){
            $("#user-name").html(resp.data.name);
            $("#user-mobile").html(resp.data.mobile);
            if (!resp.data.avatar){
                $("#user-avatar").attr("src",resp.data.avatar)
            }
        }
    },"json")
})


