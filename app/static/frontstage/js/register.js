$(function () {
    $('#pic').click(function (event){
        var self = $(this);
        var src = self.attr('src');
        var newsrc = myparam.setParam(src,'xx',Math.random());
        self.attr('src', newsrc);
    });
});
