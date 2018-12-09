//点击登录按钮触发提交表单事件
$(function (){
    $('#login_submit').click(function (event) {
        event.preventDefault();
        var Etelephone = $("input[name='telephone']");
        var Epassword = $("input[name='password']");
        //开始获取表单提交的数据
        var telephone = Etelephone.val();
        var password = Epassword.val();

        myajax.post({
            'url': '/login/',
            'data':{
                'telephone': telephone,
                'password': password
            },
            'success': function (data){
                if (data['code'] == 200)
                {
                    var referer = $("#referer").text();
                    if (referer & referer != '/register/'){
                        window.location = referer;
                    }
                    else{
                        window.location = '/';
                    }
                }
                else
                {
                    var message = data['message'];
                    lgyalert.alertInfo(message);
                    //密码出现问题，清空密码栏
                    Epassword.val("");
                }
            },
            'fail': function (error){
                lgyalert.alertError("网络错误");
            }
        });
    });
});
