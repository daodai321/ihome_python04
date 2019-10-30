$(document).ready(function(){
    $.get("/api/v1.0/users/auth",function (resp) {
        if (resp.errno=="4101"){
            location.href="/login.html"
        }else if(resp.errno=="0"){
            if (!(resp.data["real_name"]&&resp.data["id_card"])){
                $(".auth-warn").show();
                return;
            }
            $.get("/api/v1.0/user/houses",function (resp) {
                if (resp.data.errno=="0"){
                    $("#houses-list").html(template("houses-list-tmpl", {house_list:resp.data.house_list}))
                }else{
                    $("#houses-list").html(template("houses-list-tmpl", {house_list:[]}))
                }
            },"json")

        }
    },"json")


})