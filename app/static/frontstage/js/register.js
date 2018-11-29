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
    $('#sms-captcha-btn').click(function(event){
        event.preventDefault();
        var telephone = $("input[name='telephone']").val()//获取用户输入的电话号码的值

    });
});
