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
