import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from Wordoid.models import Post, Comment
from Wordoid.forms import PostForm, CommentForm
from Wordoid.utils import get_paginated_objects
from silk.profiling.profiler import silk_profile

# django-silk
@silk_profile(name='View Blog Post')
def home_page(request):
    posts = Post.objects.filter(
        publish=True).select_related(
        'auther').prefetch_related('liked_users', 'post').all()
    post_data = [{
                    "id": post.id,
                    "title": post.title,
                    "description": post.description,
                    "author": post.auther,
                    "is_liked": post.liked_users.filter(
                        id=request.user.id).exists(),
                    "like_count": post.user_like,
                    "comments": post.post.all()
                } for post in posts]
    dict_data = {
        'posts': get_paginated_objects(request, post_data),
    }
    return render(request, "post/home.html", dict_data)


@login_required
def show_post(request):
    user_post = Post.objects.filter(auther=request.user)
    dict_post = {
        'all_post': user_post
    }
    return render(request, "post/show_post.html", dict_post)


@login_required
def change_post(request, id):
    post = Post.objects.get(id=id)
    if post.publish:
        post.publish = False
    else:
        post.publish = True
    post.save()
    return redirect(publish_post)


def add_post(request):
    # code to add a post
    title = request.POST.get('"title')
    description = request.POST.get('description')
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    up_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # we have two methods to save post creat() and save()
    Post.objects.create(
        title=title, description=description,
        publish_date=today_date, update_date=up_date
        )
    ''' post_instance = Post(title=title,description=description,
        publish_date=today_date,update_date=up_date)'''
    # post_instance.save()


def post_model_form(request):
    if request.method == 'POST':
        add_post_form = PostForm(request, request.POST)
        if add_post_form.is_valid():
            instance = add_post_form.save(commit=False)
            instance.auther = request.user
            instance.save()
            return redirect(show_post)
    else:
        add_post_form = PostForm(request)
    return render(request, "post/post_form.html", {'form': add_post_form})


def publish_post(request):
    publish_post = Post.objects.filter(auther=request.user, publish=True)
    posts = get_paginated_objects(request, publish_post)
    dict_data = {
        "posts": posts,
    }
    return render(request, "post/publish_page.html", dict_data)


def unpublish_post(request):
    unpublish_post = Post.objects.filter(auther=request.user, publish=False)
    dict_data = {
        'unpublish_data': unpublish_post
    }
    return render(request, "post/unpublish_page.html", dict_data)


def view_post(request, id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        data = [{
                "title": post.title,
                "description": post.description,
                "publish_date": post.publish_date,
                "update_date": post.update_date,
                "comment": post.post.values_list('text_field')
                }]
        dict_data = {
            'data': data,
        }
        return render(request, "post/view_post.html", dict_data)
    else:
        return redirect('/accounts/signup/')


def edit_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        post_form = PostForm(request, request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect(publish_post)

    else:
        post_form = PostForm(request, instance=obj)
    return render(
            request, "post/edit_post.html",
            {'form': post_form, 'obj': post}
            )


def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect(publish_post)


def comment_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        comment = CommentForm(request.POST)
        if comment.is_valid():
            instance = comment.save(commit=False)
            instance.post = post
            instance.user = request.user
            instance.save()
            return redirect(publish_post)
    else:
        comment_form = CommentForm()
    return render(
            request, "post/comment_post.html",
            {'form': comment_form, 'obj': post}
            )


def like_post(request, id):
    like_user = False
    post = Post.objects.get(id=id)
    if not post.liked_users.filter(id=request.user.id).exists():
        post.liked_users.add(request.user)
        like_user = True
    else:
        post.liked_users.remove(request.user)
    dict_data = {
        'post_id': post.id,
        'like_value': like_user
    }
    return JsonResponse({'result': dict_data})


def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    dict_data = {
        'comment': model_to_dict(comment),
    }
    return JsonResponse({'results': dict_data, 'result': id})


def search_data(request):
    text_data = request.GET.get('text_data')
    related_post = Post.objects.filter(
        auther=request.user,
        title__icontains=text_data)
    dict_data = {
        'related_post': list(related_post.values())
    }
    return JsonResponse(dict_data)
