//发布帖子的相关js文件
//获取富文本编辑器
$(function (){
    var editor = UE.getEditor("editor", {
        'serverUrl': '/ueditor/upload/'
    });

    $("#submit-btn").click(function (event){
        event.preventDefault();

        var titleE = $("input[name='title']");
        var areaE = $("select[name='area']");

        var theme = titleE.val();
        var area_id = areaE.val();
        var content = editor.getContent();//获取用户输入的内容 包括样式

        myajax.post({
            'url': '/addpost/',
            'data':{
                'theme': theme,
                'content': content,
                'area_id': area_id
            },
            'success': function(data){
                if (data['code'] == 200){
                    lgyalert.alertSuccessToast("帖子发布成功");
                    window.location = '/';
                }
                else{
                    lgyalert.alertInfo(data['message']);
                }
            },
            'fail': function(error){
                lgyalert.alertError("网络错误");
            }
        });


    });

});
