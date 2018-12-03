//根据url的位置，使左边框有点击效果
$(function () {
    var url = window.location.href;
    if(url.indexOf('selfinfo') >= 0){
        var infoManage = $('.is_active_info');
        infoManage.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('carousel') >= 0){
        var carouselManage = $('.is_active_carousel');
        carouselManage.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('forum') >= 0){
        var forumManage = $('.is_active_forum');
        forumManage.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('password') >= 0){
        var passwordManage = $('.is_active_info');
        passwordManage.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('resetemail') >= 0){
        var mailManage = $('.is_active_info');
        mailManage.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('comment') >= 0){
        var commentManage = $('.is_active_comment');
        commentManage.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('area') >= 0){
        var areaManage = $('.is_active_area');
        areaManage.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('user') >= 0){
        var userManage = $('.is_active_user');
        userManage.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('mancms') >= 0) {
        var cmsuserManage = $('.is_active_cmsuser');
        cmsuserManage.addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('auth') >= 0){
        var groupManage = $(".is_active_group");
        groupManage.addClass('active').siblings().removeClass('active');
    }
});
