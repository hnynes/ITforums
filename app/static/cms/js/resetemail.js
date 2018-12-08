$(function () {
    //获取验证码按钮，当点击之后会触发后台去给输入的邮箱账户发送带有验证码的邮件
    $("#sendcaptcha").click(function (event){
        //禁止默认的表单提交方式
        event.preventDefault();
        var ele1 = $("input[name='newemail']");//输入邮箱那个标签
        var newemail = ele1.val();
        if (!newemail)//用户未输入邮箱时点击获取验证码按钮
        {
            lgyalert.alertInfoToast("请输入邮箱");
            return;
        }
        //以get形式向后台发送数据
        myajax.get({
            'url' :'/cms/sendcaptcha/',
            'data':{
                'email': newemail
            },
            'success': function (data) {
                if (data['code'] == 200)
                {
                    lgyalert.alertSuccessToast("验证码发送成功！");
                }
                else
                {
                    lgyalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                lgyalert.alertError("网络出了点小问题");
            }
        });
    });
});

//捕捉提交修改按钮
$(function () {
    //捕捉按钮点击事件
    $("#submit").click(function (event) {
        event.preventDefault();
        var ele1 = $("input[name='newemail']");
        var ele2 = $("input[name='captcha']");

        var email = ele1.val();
        var captcha = ele2.val();

        myajax.post({
            'url' :'/cms/resetemail/',
            'data':{
                'email': email,
                'captcha': captcha
            },
            'success': function (data){
                if (data['code'] == 200)
                {
                    lgyalert.alertSuccessToast("邮箱修改成功");
                }
                else
                {
                    lgyalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                lgyalert.alertError("网络出了点小问题");
            }
        });
    });
});
