/*
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: myalert.js
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-21 23:52:50 (CST)
# Last Update:
#          By:
# Description: 基于sweetalert封装的js文件，目的是为更加方面自己在开发过程中调用
# **************************************************************************
*/

var lgyalert = {
    /*
     * 出错信息提示框
     * msg :提示的内容
     */
    'alertError': function (msg) {
        swal('提示', msg, 'error');
    },
    /*
     * 通知信息提示框
     * msg：提示的内容
     */
    'alertInfo':function (msg) {
        swal('提示', msg, 'warning');
    },
    /*
     * 可以自定义标题的信息提示框
     * msg：提示的内容（可选）
     */
    'alertInfoWithTitle': function (title,msg) {
        swal(title, msg);
    },
    /*
     * 成功的信息提示框
     * msg：提示的内容（必须）
     * confirmCallback：点击提示框的确认按钮
     */
    'alertSuccess':function (msg,confirmCallback) {
        args = {
            'title': '提示',
            'text': msg,
            'type': 'success',
        }
        swal(args,confirmCallback);
    },
    /*
     * 带有标题的成功信息提示框
     * title：提示框的标题（必须）
     * msg：提示的内容（必须）
     */
    'alertSuccessWithTitle':function (title,msg) {
        swal(title,msg,'success');
    },
    /*
        功能：确认提示
        参数：字典的形式
            - title：提示框标题（可选）
            - type：提示框的类型（可选）
            - confirmText：确认按钮文本（可选）
            - cancelText：取消按钮文本（可选）
            - msg：提示框内容（必须）
            - confirmCallback：确认按钮点击回调（可选）
            - cancelCallback：取消按钮点击回调（可选）
    */
    'alertConfirm':function (params) {
        swal({
            'title': params['title'] ? params['title'] : '提示',
            'showCancelButton': true,
            'showConfirmButton': true,
            'type': params['type'] ? params['type'] : '',
            'confirmButtonText': params['confirmText'] ? params['confirmText'] : '确定',
            'cancelButtonText': params['cancelText'] ? params['cancelText'] : '取消',
            'text': params['msg'] ? params['msg'] : ''
        },function (isConfirm) {
            if(isConfirm){
                if(params['confirmCallback']){
                    params['confirmCallback']();
                }
            }else{
                if(params['cancelCallback']){
                    params['cancelCallback']();
                }
            }
        });
    },
    /*
        功能：带有一个输入框的提示
        参数：字典的形式
            - title：提示框的标题（可选）
            - text：提示框的内容（可选）
            - placeholder：输入框的占位文字（可选）
            - confirmText：确认按钮文字（可选）
            - cancelText：取消按钮文字（可选）
            - confirmCallback：确认后的执行事件
    */
    'alertOneInput': function (params) {
        swal({
            'title': params['title'] ? params['title'] : '请输入',
            'text': params['text'] ? params['text'] : '',
            'type':'input',
            'showCancelButton': true,
            'animation': 'slide-from-top',
            'closeOnConfirm': false,
            'showLoaderOnConfirm': true,
            'inputPlaceholder': params['placeholder'] ? params['placeholder'] : '',
            'confirmButtonText': params['confirmText'] ? params['confirmText'] : '确定',
            'cancelButtonText': params['cancelText'] ? params['cancelText'] : '取消',
        },function (inputValue) {
            if(inputValue === false) return false;
            if(inputValue === ''){
                swal.showInputError('输入框不能为空！');
                return false;
            }
            if(params['confirmCallback']){
                params['confirmCallback'](inputValue);
            }
        });
    },
    /*
     * 网络错误提示框
     */
    'alertNetworkError':function () {
        this.alertErrorToast('网络错误');
    },
    /*
     * 信息toast提示 toast提示代表会自动消失的信息提示框
     * msg：提示消息
     */
    'alertInfoToast':function (msg) {
        this.alertToast(msg,'info');
    },
    /*
     * 错误toast提示
     * msg：提示消息
     */
    'alertErrorToast':function (msg) {
        this.alertToast(msg,'error');
    },
    /*
     * 成功toast提示（1s后消失）
     * msg：提示消息
     */
    'alertSuccessToast':function (msg) {
        if(!msg){msg = '成功！';}
        this.alertToast(msg,'success');
    },
    /*
        功能：弹出toast（1s后消失）
        参数：
            - msg：提示消息
            - type：toast的类型
    */
    'alertToast':function (msg,type) {
        swal({
            'title': msg,
            'text': '',
            'type': type,
            'showCancelButton': false,
            'showConfirmButton': false,
            'timer': 1000,
        });
    },
    // 关闭当前对话框
    'close': function () {
        swal.close();
    }
};
