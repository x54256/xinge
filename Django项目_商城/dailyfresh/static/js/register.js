$(function(){

	var error_name = false;
	var error_password = false;
	var error_check_password = false;
	var error_email = false;
	var error_check = false;


	$('#user_name').blur(function() {		// 当user_name标签失去焦点时，触发下面的事件
		check_user_name();
	});

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	$('#email').blur(function() {
		check_email();
	});

	$('#allow').click(function() {
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
	});


	function check_user_name(){
		var len = $('#user_name').val().length;
		if(len<5||len>20)
		{
			$('#user_name').next().html('请输入5-20个字符的用户名');	// 为user_name下一个标签赋予文本内容
			$('#user_name').next().show();		// 将为user_name下一个标签（隐藏的标签,display=none）显示出来
			error_name = true;
		}
		else
		{
			$('#user_name').next().hide();		// 将为user_name下一个标签隐藏
			error_name = false;
		}
	}

	function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<8||len>20)
		{
			$('#pwd').next().html('密码最少8位，最长20位')
			$('#pwd').next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}		
	}


	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('两次输入的密码不一致')
			$('#cpwd').next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}		
		
	}

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;		// 定义re匹配

		if(re.test($('#email').val()))		// 如果符合该正则匹配
		{
			$('#email').next().hide();
			error_email = false;
		}
		else
		{
			$('#email').next().html('你输入的邮箱格式不正确')
			$('#email').next().show();
			error_check_password = true;
		}

	}

	// $('#register_form').submit(function() {	 // 点提交的时候再检查一下
	// 	check_user_name();
	// 	check_pwd();
	// 	check_cpwd();
	// 	check_email();
    //
	// 	if(error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false)
	// 	{
	// 		return true;	 // 如果全符合，返回True 可以提交表单
	// 	}
	// 	else
	// 	{
	// 		return false;
	// 	}
    //
	// });

})