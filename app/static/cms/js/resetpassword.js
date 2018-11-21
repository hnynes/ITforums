
$(function () {
    //获取按钮
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
                console.log(data);
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    });
});
