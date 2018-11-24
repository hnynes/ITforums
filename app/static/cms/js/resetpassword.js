//在这里使用了=jQuery.min.js
//即$();等价于jQuery();因此在使用此js代码之前要先引入jquery.min.js文件否则会报错。jQuery(function ());可以接收一个函数
$(function () {
    //获取按钮  当用户点击提交更改时,会触发event事件
    $("#submit").click(function (event) {
        //因为是以aljx方式提交表单数据，因此需要禁止表单的默认提交
        event.preventDefault();

        //获取表单输入的数据
        var ele1 = $("input[name=oldpassword]");
        var ele2 = $("input[name=newpassword]");
        var ele3 = $("input[name=newpassword2]");

        var oldpwd = ele1.val();
        var newpwd = ele2.val();
        var newpwd2 = ele3.val();

        myajax.post({
            'url': '',
            'data':{
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                if (data['code'] == 200)
                {
                    //如果修改密码成功
                    lgyalert.alertSuccessToast("密码修改成功");
                    ele1.val("");
                    ele2.val("");
                    ele3.val("");
                }
                else
                {
                    var message = data['message'];
                    lgyalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                lgyalert.alertError("网络错误");
            }
        });
    });
});
