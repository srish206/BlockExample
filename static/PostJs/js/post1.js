$(document).ready(function(){
    $(document).on('click', '.add_post', function(){
        form_data=$('form').serialize()
        $.ajax({
                type: "POST",
                url: "/add-post",
                data: JSON.stringify(form_data),
                success:function(){
            }
        });
    });

});
