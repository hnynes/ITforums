//点击验证码会更新不同的验证码
$(function() {
    $('#pic').click(function(event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = myparam.setParam(src, 'xx', Math.random());
        self.attr('src', newsrc); //jquery中的attr用法 即 将'src'替换为newsrc中生成的随机值，从而点击一次达到获取不同验证码的功能
    });
});
//点击发送验证码时触发事件
$(function() {
    $('#sms-captcha-btn').click(function(event) {
        event.preventDefault();
        var telephone = $("input[name='telephone']").val(); //获取用户输入的电话号码的值
        //主要实现的功能是在发送验证码的120秒内不能再发送验证码，按钮变成倒计时状态
        var self = $(this); //获取按钮本身
        var timestamp = (new Date).getTime();//获取当时的时间
        var salt = 'test123*asdsfasdsfas';
        var sign = md5(timestamp + telephone + salt);
        //利用正则表达式检验手机号码的正确性
        if (!(/^1[345879]\d{9}$/.test(telephone))) {
            lgyalert.alertInfoToast("请输入正确的手机号码!");
            return;
        } else {
            myajax.post({
                'url': '/common/sendmessage/',
                'data':{
                    'telephone': telephone,
                    'timestamp': timestamp,
                    'sign': sign
                },
                'success': function(data) {
                    if (data['code'] == 200) {
                        lgyalert.alertSuccessToast("验证码发送成功！");
                        self.attr('disabled', 'disabled'); //替换按钮的属性
                        var time = 120;
                        //为了实现及时功能，需要使用setInterval函数来周期性的执行-1操作从而达到计时功能 ,后面的参数设置为1000已实现每一秒-1
                        var count = setInterval(function(){
                            time--;
                            self.text(time);
                            //当计时器时间用完，用户可以重新发送验证码
                            if (time <= 0){
                                self.removeAttr('disabled');//移除按钮不可用属性
                                clearInterval(count);//移除计时器函数
                                self.text('发送验证码');
                            }
                        }, 1000);
                    } else {
                        lgyalert.alertInfo(data['message']);
                    }
                }
            });
        }
    });
});

//点击立即注册按钮触发提交表单事件
$(function (){
    $('#reg_submit').click(function (event) {
        event.preventDefault();
        var Etelephone = $("input[name='telephone']");
        var Emessagecode = $("input[name='validate']");
        var Eusername = $("input[name='username']");
        var Epassword1 = $("input[name='password1']");
        var Epassword2 = $("input[name='password2']");
        var Epicturecode = $("input[name='picture_validate']");
        //开始获取表单提交的数据
        var telephone = Etelephone.val();
        var messagecode = Emessagecode.val();
        var username = Eusername.val();
        var password1 = Epassword1.val();
        var password2 = Epassword2.val();
        var picturecode = Epicturecode.val();

        myajax.post({
            'url': '/register/',
            'data':{
                'telephone': telephone,
                'messagecode': messagecode,
                'username': username,
                'password1': password1,
                'password2': password2,
                'picturecode': picturecode
            },
            'success': function (data){
                if (data['code'] == 200)
                {
                    lgyalert.alertSuccessToast("注册成功");
                    var referer = $("#referer").text();
                    if (referer){
                        window.location = '/login/';
                    }
                    else{
                        window.location = '/';
                    }
                }
                else
                {
                    var message = data['message'];
                    lgyalert.alertInfo(message);
                    //跳转到此逻辑时说明用户注册还未完成，此时清空用户已经输入的内容
                    Emessagecode.val("");
                    Epassword1.val("");
                    Epassword2.val("");
                    Etelephone.val("");
                    Eusername.val("");
                    Epicturecode.val("");

                }
            },
            'fail': function (error){
                lgyalert.alertError("网络错误");
            }
        });
    });
});
