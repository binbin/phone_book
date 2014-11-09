$(function(){
	$('.phone_feild a').click(function(){
		$.get('/delete',{key:$(this).data('key')})
		$(this).parent().fadeOut()
	})
})