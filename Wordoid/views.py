import json
import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.template import loader
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from Wordoid.models import Post, Comment
from Wordoid.forms import PostForm, CommentForm



# @csrf_exempt
def home_page(request):
    post_data = []
    posts = Post.objects.filter(publish=True).select_related('auther').prefetch_related('post').all()
    for post in posts:
        post_data.append({
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "author": post.auther,
                "is_liked": post.liked_users.filter(id=request.user.id).exists(),
                "like_count": post.user_like,
                "comments": post.post.all(),
            })

    page = request.GET.get('page', 1)
    paginator = Paginator(post_data, settings.PAGE_COUNT)

    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
            posts_page = paginator.page(paginator.num_pages)
    dict_data = {
        'posts': posts_page,
    }
    return render(request, "post/home.html", dict_data)



# @csrf_exempt
@login_required
def show_post(request):
    show_all_post = Post.objects.filter(auther=request.user)
    dict_post = {
        'all_post': show_all_post
    }
    return render(request, "post/show_post.html", dict_post)


# @csrf_exempt
@login_required
def change_post(request, id):
    post = Post.objects.get(id=id)
    if post.publish:
        post.publish = False
    else:
        post.publish = True
    post.save()
    return redirect(publish_post)


# @csrf_exempt
def add_post(request):
    # code to add a post
    title = request.POST.get('"title')
    description = request.POST.get('description')
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    up_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # we have two methods to save post creat() and save()
    post_instance = Post.objects.create(
        title=title, description=description,
        publish_date=today_date, update_date=up_date
        )
    # post_instance = Post(title=title,description=description,publish_date=today_date,update_date=up_date)
    # post_instance.save()


# @csrf_exempt
def post_model_form(request):

    if request.method == 'POST':
        post_form = PostForm(request, request.POST)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.auther = request.user
            instance.save()
            return redirect(show_post)
    else:
        post_form = PostForm(request)
    return render(request, "post/post_form.html", {'form': post_form})


# @csrf_exempt
def publish_post(request):
    current_user = request.user
    user_post = Post.objects.filter(auther=current_user, publish=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(user_post, settings.PAGE_COUNT)

    try:
        user_post = paginator.page(page)
    except PageNotAnInteger:
        user_post = paginator.page(1)
    except EmptyPage:
            user_post = paginator.page(paginator.num_pages)
    
    dict_data = {
        "posts": user_post,
    }
    return render(request, "post/publish_page.html", dict_data)



# @csrf_exempt
def unpublish_post(request):
    unpublish_data = Post.objects.filter(publish=False)
    dict_data = {
        'unpublish_data': unpublish_data
    }
    return render(request, "post/unpublish_page.html", dict_data)


def view_post(request, id):
    if request.user.is_authenticated:
        data = []
        comment = []
        obj = Post.objects.get(id=id)
        data.append({
                        "title": obj.title,
                        "description": obj.description,
                        "publish_date": obj.publish_date,
                        "update_date": obj.update_date,
                    })
        comment = obj.post.values_list('text_field')
        dict_data = {
            'data': data,
            'comment': comment
        }
        return render(request, "post/view_post.html", dict_data)    
    else:
        return redirect('/accounts/signup/')


def edit_post(request, id):
    obj = Post.objects.get(id=id)
    if request.method == 'POST':
        obj_form = PostForm(request, request.POST, instance=obj)
        if obj_form.is_valid():
            obj_form.save()
            return redirect(publish_post)
    
    else:
        obj_form = PostForm(request, instance=obj)
    return render(request, "post/edit_post.html", {'form': obj_form, 'obj': obj})


def delete_post(request, id):
    obj = Post.objects.get(id=id)
    obj.delete()
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
        obj_form = CommentForm()
    return render(request, "post/comment_post.html", {'form': obj_form,'obj': post})


# @csrf_exempt
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
    related_post = Post.objects.filter(auther=request.user, title__icontains=text_data)
    dict_data = {
        'related_post':list(related_post.values())
    }
    return JsonResponse(dict_data)



# class Index:
#     def __init__(self, name):
#         self.name = name

#     def say(self, msg):
#         print(f"hello {msg}!")

# class ShowPost(Index):
    
#     def say(self, msg):
#         print(f"hello {msg}!")

# p = Parent()
# print(p.say('srishti'))

# c = Child()
# print(c.say('akshay'))