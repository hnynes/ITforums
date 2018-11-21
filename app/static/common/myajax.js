
/*************************************************************************
 Copyright © superliuliuliu1
 File Name: manage.py
 Author: superliuliuliu1
 Email: superliuliuliu1@gmail.com
 Created: 2018-11-20 21:20:50 (CST)
 Last Update:
        By:
 Description:对jquery的ajax的封装 包含防止CSRF攻击
# AJAX(ajax)
# Async JavaScript And XML
# Async（异步）：网络请求是异步的。
# JavaScript：JavaScript语言
# And：并且
# XML：JSON
**************************************************************************/

'use strict';
var myajax = {
	'get':function(args) {
		args['method'] = 'get';
		this.ajax(args);
	},
	'post':function(args) {
		args['method'] = 'post';
		this.ajax(args);
	},
	'ajax':function(args) {
		// 设置csrftoken
		this._ajaxSetup();
		$.ajax(args);
	},
	'_ajaxSetup': function() {
		$.ajaxSetup({
			'beforeSend':function(xhr,settings) {
				if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    var csrftoken = $('meta[name=csrf-token]').attr('content');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
			}
		});
	}
};
