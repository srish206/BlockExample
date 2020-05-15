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
    comment_id = $(this).data('comment')
    $(".replay-cls[data-comment]").each(function(index){
        if($(this).data('comment') == comment_id){
            $(this).siblings('div').children().first().removeClass('hide')
            $(this).siblings('div').toggle()
        }
    })
})

    

$(document).on('click', '.rep',function(){
    // $('#info-table').append()
    // $('#info-table').append("<input type='text'/>");
    // $("<input type='text' />").appendTo('#info-table');
    var csrf_token = $('meta[name="csrf-token"]').attr('content');
    rep_id = $(this).data('rep')
    $(".rep[data-rep]").each(function(index){
        if($(this).data('rep') == rep_id){
            $(this).siblings('div').append('<form id="mySearch"></form>');
                $('#mySearch').attr("action","").attr("method","post").attr('name','csrf_token')
                .append("<input type='hidden' name='parent_id' value='"+rep_id+"' >" +
                    "<input type='text' value='' class='txt-cls'/>" + '<input type="submit" class="sub-cls" value="Repllllly">'
                    );
        }
    })
})

// $(document).on('click','.sub-cls',function(){
//     var csrftoken = $("[name=csrfmiddlewaretoken]").val();
//     // var token =  $('input[name="csrfToken"]').attr('value'); 
//     rep_id = $('.rep').data('rep')
//     // rep_data=$('.txt-cls').val()
//     rep_data=$('form').serialize()
//     // rep_data=$('#mySearch').serialize()
//     post_id=$('.rep').data('post')
//     $.ajax({
//         type: "POST",
//         headers: {
//                     'X-CSRFToken': csrftoken 
//                },
//         url: "/comment-post/" + post_id,
//         data: {
//             "text_field": rep_data,
//             "parent_id": rep_id
//         },
//         success: function(){

//         }
//     })

// })


$(document).on('click','.sub-cls ',function(e){
    e.preventDefault();
    rep_id = $("input[name=parent_id]").val();
    rep_data=$('.txt-cls').val();
    post_id=$('.rep').data('post')
    $.ajax({
        type: "POST",
        url: "/comment-post/" + post_id,
        data: {
            "text_field": rep_data,
            "parent_id": rep_id
        },
        success: function(result){
            aa=result.result.lists[0].text_field
            if($('.rep').data('rep') == result.result.parent_id){
                $('#comment_add').append(
                        "<div>" + 
                            "<ul>" + aa + "</ul>" 
                        + "</div>"
                )
                    
            }

        }
    })

})











// <ul>
//     {% for comm in post.comments %}
//     <div data-comm="{{ comm.id }}">
//         <li>{{ comm.text_field }}<br>
//             <a data-rep="{{ comm.id }}" data-post="{{ post.id }}" class="rep">Rep</a>
//         </li>
//         {% if comm.replies.exists %}
//             <ul>
//                 {% with comm.replies.all as tags %}
//                     {% for tag in tags %}
//                         {{ tag.text_field }}<br>
//                         <a data-rep="{{ tag.id }}" data-post="{{ post.id }}" class="rep">Rep</a><br>
//                     {% endfor %}
//                 {% endwith %}<br>
//             </ul> 
//         {% endif %}
//     </div>
//     {% endfor %}
// </ul>













