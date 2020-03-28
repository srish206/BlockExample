$(document).ready(function(){
    $(document).on('click','.commen-cls',function(){
        post_id=$(this).parent().parent().attr('data-post')
        // const _this = this;
        $.ajax({
                type:"GET",
                url:"/like-post/" + post_id,
                data:post_id,
                success:function(result){
                    post_id=result.result.post_id
                    like=result.result.like_value
                        if(like == false){
                            $(".list-cls[data-post]").each(function(index){
                                if($(this).data('post') == post_id){
                                    $(this).children('span').children('i').removeClass('heart-cls')
                                    $(this).children('span').children('i').addClass('none-cls')
                                }
                            });
                        }
                        else if(like == true){
                            $(".list-cls[data-post]").each(function(index){
                                if($(this).data('post') == post_id){
                                    $(this).children('span').children('i').removeClass('none-cls')
                                    $(this).children('span').children('i').addClass('heart-cls')
                                }
                            });
                        }
                }
        });
    });
});
