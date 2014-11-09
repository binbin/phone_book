$(function(){
      	$('input').eq(0).focus()
      	$.validator.addMethod("isPhone", function(value,element) {   
    	      var length = value.length;   
    	      var mobile = /^1[3|4|5|7|8|][0-9]{9}$/;     
    	      return this.optional(element) || mobile.test(value);   

    	}, "请输入正确的手机号码"); 
    	$.validator.addMethod("chinese", function(value,element) {   
    	      var length = value.length;   
    	      var chinese = /^[\u4e00-\u9fa5]+$/;     
    	      return this.optional(element) || chinese.test(value);   

    	}, "此字段应全部为汉字"); 

        $('#sub').click(function(){
			$('#form1').submit()
		})
		$('#form1').keyup(function(event){
			if(event.keyCode===13){
			  $('#form1').submit();
			}
		})
		var validater = $('#form1').validate({
			submitHandler: function(form){
		     	form.submit();
		    },
		    rules:{
		    	'name':{
		    	   required:true,
                   maxlength:8,
                   minlength:2,
                   chinese:true
		    	},
		    	'phone':{
		    		required:true,
		    		isPhone:true
		    	},
		    	'department':{
		    		required:true,
		    		maxlength:30,
                    minlength:4,
                    chinese:true
		    	}
		    },
		    messages:{
		    	'name':{
		    		required:'请填写您的名字',
		    		maxlength:'本班内名字最长的也没有这么长',
		    		minlength:'没有这么短的名字'
		    	},
		    	'phone':{
                    required:'请填写您的手机',
		    	},
		    	'department':{
		    		required:'请填写您的工作单位',
		    		maxlength:'请正确输入单位名称(至多30个字)',
		    		minlength:'请正确输入单位名称(至少4个字)'
		    	}
		    },
		    focusInvalid: true,
	        onkeyup: false,
	        errorClass: "error",
	        wrapper:'span',
	        errorPlacement: function(error, element){
                element.after(error)
            }
		})
      })