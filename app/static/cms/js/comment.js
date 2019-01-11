//对应删除评论的按钮
$(function (){
    $(".delete-comment-btn").click(function (event){
    event.preventDefault();
    var self = $(this);
    var tr = self.parent().parent();
    var com_id = tr.attr("data-id");
    lgyalert.alertConfirm({
        'msg':"确认要执行删除操作？",
        'confirmCallback': function(){
            myajax.post({
                'url': '/cms/delcomment/',
                'data':{
                    'com_id': com_id
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
