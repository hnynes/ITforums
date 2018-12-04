//点击保存按钮触发的事件
$(function () {
    $("#commit-btn").click(function (event) {
        event.preventDefault();

        var dialog = $("#fixdialog");
        var nameE = $("#inputname");
        var pic_urlE = $("#picture");
        var next_urlE = $("#URL");
        var weightE = $("#weight");

        var name = nameE.val();
        var pic_url = pic_urlE.val();
        var next_url = next_urlE.val();
        var weight = weightE.val();

        if (!name || !pic_url || !next_url || !weight){
            lgyalert.alertError("您填写的信息不完整！");
            return;
        }
        myajax.post({
            'url':'/cms/addcarousel/',
            'data':{
                'name': name,
                'pic_url': pic_url,
                'next_url': next_url,
                'weight': weight
            },
            'success': function(data) {
                //提交成功后隐藏对话框
                dialog.modal("hide");
                if (data['code'] == 200){
                    window.location.reload();//提交成功的话重新加载该页面
                }
                else{
                    var message = data['message'];
                    lgyalert.alertInfo(message);
                }
            },
            'fail': function(error) {
                lgyalert.alertError("网络错误")
            }
        });

    });
});
