$(document).ready(function(){
	$(document).on('search', '.form-control', function(){
		text=$('.form-control').val()
		$.ajax({
				type: "GET",
				url: "/search-data",
				data: {
						'text_data': text
				},
				success:function(result){
					data=result.related_post
					$('.list-cls').remove();
					$(data).each(function(index){
						data_index=data[index]
						$(data_index).each(function(row){
							$('#post-id').append(
								'<li class="list-cls col-md-4" style="background-color:white; width: 50%;" data-post='+data_index.id+'>\
								Post Title: '+data_index.title+'\
						 		<br>Description:'+data_index.description+'<br>\
						 		like count:'+data_index.user_like+'<br></li>')
							})
					})
				}
			});
		});
});