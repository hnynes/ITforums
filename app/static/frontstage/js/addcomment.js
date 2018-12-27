$(function (){
    var editor = UE.getEditor("editor", {
        'serverUrl': '/ueditor/upload/',
         toolbars: [[
            'source',
            'undo',
            'redo',
            'bold',
            'simpleupload', //图片上传
            'emotion' //表情
       ]]
    });
    window.editor = editor;
});

$(function () {
    $("#btn-comment").click(function (event){
        event.preventDefault();
        var logintag = $("#login-tag").attr("userlogin");
        if (!logintag)
        {
            window.location = '/login/';
        }
        else
        {
            var comment = window.editor.getContent();
            var post_id = $("#post-content").attr("data-id");
            myajax.post({
                'url': '/addcomment/',
                'data': {
                    'content': comment,
                    'post_id': post_id
                },
                'success': function(data){
                    if (data['code'] == 200)
                    {
                        window.location.reload();
                    }
                    else
                    {
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
