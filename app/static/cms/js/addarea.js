$(function (){
    $("#commit-btn").click(function (event){
        event.preventDefault();

        var self = $(this);
        var dialog = $("#fixdialog");
        var nameE = dialog.find("#inputname");

        var name = nameE.val();
        var type = self.attr("data-type");
        var id = self.attr("data-id");

        if (!name){
            lgyalert.alertError("请填入完整的信息！");
            return;
        }

        var url = '';
        if (type == "update"){
            url = '/cms/uarea/';
        }
        else{
            url = '/cms/addarea/';
        }

        myajax.post({
            'url': url,
            'data':{
                'name': name,
                'area_id': id
            },
            'success': function(data){
                dialog.modal("hide");
                if (data['code'] == 200){
                    window.location.reload();
                }
                else{
                    lgyalert.alertInfo(data['message'])
                }
            },
            'fail': function(error){
                lgyalert.alertError("网络错误")
            }
        });

    });
});

$(function (){
    $(".edit-area-btn").click(function (event){
        var self = $(this);
        var dialog = $("#fixdialog");

        dialog.modal("show");
        var tr = self.parent().parent();
        var name = tr.attr('data-name');

        var nameE = dialog.find("#inputname");
        var button = dialog.find("#commit-btn");
        nameE.val(name);

        button.attr("data-type", "update");
        button.attr("data-id", tr.attr("data-id"));


    });
});

$(function (){
    $(".delete-area-btn").click(function (event){
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var id = tr.attr('data-id');
        lgyalert.alertConfirm({
            'msg':"确认要执行删除操作？",
            'confirmCallback': function(){
                myajax.post({
                    'url': '/cms/delarea/',
                    'data':{
                        'area_id': id
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
