$(document).ready(function(){
    $(document).on('click', '.delete-cls', function(){
        comment_id=$(this).attr('data-id')
        $.ajax({
                type: "GET",
                url: "/delete-comment/" + comment_id,
                data: comment_id,
                success: function(result){
                    post_id=result.results.comment.post
                    result_id=result.result
                    $(".list-cls[data-post] ").each(function(index){
                        if($(this).data('post') == post_id){
                            ab=$(this).children('div').children()
                            $(ab).each(function(index){
                                $(".delete-cls[data-id]").each(function(index){
                                    if($(this).data('id') == result_id){
                                        $(this).parent().remove()
                                        }
                                });

                            }); 
                        
                        }

                    }); 
                }
            }); 
        })
})

$(document).on('click', '.replay-cls', function(){
    debugger
    comment_id = $(this).data('comment')
    $(".replay-cls[data-comment]").each(function(index){
        if($(this).data('comment') == comment_id){
            $(this).siblings('div').children().first().removeClass('hide')
            $(this).siblings('div').toggle()
        }

    })
})
