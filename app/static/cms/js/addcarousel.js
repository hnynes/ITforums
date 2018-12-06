//点击保存轮播图修改触发的事件
$(function () {
    $("#commit-btn").click(function (event) {
        event.preventDefault();

        var self = $(this);
        var dialog = $("#fixdialog");
        var nameE = dialog.find("#inputname");
        var pic_urlE = dialog.find("#picture");
        var next_urlE = dialog.find("#URL");
        var weightE = dialog.find("#weight");

        var name = nameE.val();
        var pic_url = pic_urlE.val();
        var next_url = next_urlE.val();
        var weight = weightE.val();
        var type = self.attr("data-type");
        var id = self.attr("data-id");

        if (!name || !pic_url || !next_url || !weight){
            lgyalert.alertError("您填写的信息不完整！");
            return;
        }
        var url = '';
        if (type == "update"){
            url = '/cms/ucarousel/';
        }else{
            url = '/cms/addcarousel/';
        }

        myajax.post({
            'url':url,
            'data':{
                'name': name,
                'pic_url': pic_url,
                'next_url': next_url,
                'weight': weight,
                'carousel_id': id
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

//对应点击修改轮播图按钮事件
$(function () {
    $(".edit-carousel-btn").click(function (event) {
        //event.preventDefault();
        //获取按钮本身
        var self = $(this);
        var dialog = $("#fixdialog");

        dialog.modal("show");//编辑轮播图对话框
        //获取对话框中存储的属性
        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var picture = tr.attr("data-picture");
        var next = tr.attr("data-next");
        var weight = tr.attr("data-weight");

        var nameE = dialog.find("#inputname");
        var pic_urlE = dialog.find("#picture");
        var next_urlE = dialog.find("#URL");
        var weightE = dialog.find("#weight");
        var button = dialog.find("#commit-btn");

        //将获取的属性填充到模态对话框中
        nameE.val(name);
        pic_urlE.val(picture);
        next_urlE.val(next);
        weightE.val(weight);
        button.attr("data-type", "update");//button新增属性type
        button.attr("data-id", tr.attr("data-id"));//button新增属性id 用来表示是向哪一个轮播图更新数据

    });
});

//点击删除按钮触发事件
$(function () {
    $(".delete-carousel-btn").click(function (event){
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var id = tr.attr('data-id');
        lgyalert.alertConfirm({
            'msg':"确认要执行删除操作？",
            'confirmCallback': function(){
                myajax.post({
                    'url': '/cms/delcarousel/',
                    'data':{
                        'carousel_id': id
                    },
                    'success': function(data) {
                        if (data['code'] == 200){
                            window.location.reload();
                        }
                        else{
                            lgyalert.alertInfo(data['message']);
                        }
                    },
                    'fail': function(error){
                        lgyalert.alertError("网络错误")
                    }
                });
            }
        });

    });

});
//点击选择图片按钮触发事件
