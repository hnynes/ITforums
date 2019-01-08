//对应加精、取消加精按钮
$(function (){
    $(".fine-btn").click(function (event){
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var isfine = parseInt(tr.attr("data-jingpin"));
        var url = "";
        if (isfine){
            url = "/cms/disfineforum/";
        }
        else{
            url = "/cms/fineforum/";
        }

        myajax.post({
            'url': url,
            'data':{
                'post_id':post_id
            },
            'success': function(data){
                if(data['code'] == 200){
                    lgyalert.alertSuccessToast("操作成功");
                    window.location.reload();
                }
                else{
                    lgyalert.alertInfo(data['message']);
                }
            },
            'fail':function(error){
                    lgyalert.alertError("网络错误");
            }
        });
    });
});

//对应删除帖子的按钮
$(function (){
    $(".delete-btn").click(function (event){
    event.preventDefault();
    var self = $(this);
    var tr = self.parent().parent();
    var post_id = tr.attr("data-id");
    lgyalert.alertConfirm({
        'msg':"确认要执行删除操作？",
        'confirmCallback': function(){
            myajax.post({
                'url': '/cms/delpost/',
                'data':{
                    'post_id': post_id
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
                    lgyalert.alertError("网络错误");
                }
            });
        }
    });
    });
});

//对应用户的禁言解除禁言按钮
$(function (){
    $(".forbidden-user-btn").click(function (event){
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var telephone = tr.attr("data-id");
        var islock = parseInt(tr.attr("data-jinyan"));
        var url = "";
        if (islock)
        {
            url = "/cms/unlock/user/";
        }
        else
        {
            url = "/cms/lock/user/";
        }
        myajax.post({
            'url': url,
            'data':{
                'telephone':telephone
            },
            'success': function(data){
                if(data['code'] == 200){
                    lgyalert.alertSuccessToast("操作成功");
                    window.location.reload();
                }
                else{
                    lgyalert.alertInfo(data['message']);
                }
            },
            'fail':function(error){
                    lgyalert.alertError("网络错误");
            }
        });
    });
});
