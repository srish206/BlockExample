import datetime
from silk.profiling.profiler import silk_profile
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import model_to_dict
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from Wordoid.models import Post, Comment, UserProfile
from Wordoid.forms import PostForm, CommentForm, ReaderSignUpForm
from Wordoid.utils import get_paginated_objects


def user_signup(request):
    form = ReaderSignUpForm()
    if request.method == "POST":
        form = ReaderSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=password)
            role = request.POST.get('user_type')
            profile = UserProfile.objects.create(user=user, role=role)
            ct = ContentType.objects.get_for_model(Post)
            permission = Permission.objects.get(
                codename='can_add_post',
                name='can add a post',
                content_type=ct)
            role = request.POST.get('user_type')
            group = role or "Default"
            g, created = Group.objects.get_or_create(name=group)
            if profile.role == "author":
                g.permissions.add(permission)
                user.user_permissions.add(permission)
            g.user_set.add(user)
            login(request, user)
            return redirect(home_page)
    else:
        form = ReaderSignUpForm()
        return render(request, "post/signup.html", {'form': form})


@silk_profile(name='View Blog Post')
def home_page(request):
    posts = Post.objects.filter(
        publish=True).select_related(
        'auther').prefetch_related('liked_users', 'post').all()
    post_data = [{
                    "id": post.id,
                    "title": post.title,
                    "description": post.description,
                    "des_len": len(post.description),
                    "date": post.publish_date,
                    "author": post.auther,
                    "is_liked": post.liked_users.filter(
                        id=request.user.id).exists(),
                    "like_count": post.user_like,
                    "comments": post.post.all(),
                } for post in posts]

    posts_data = get_paginated_objects(request, post_data)

    comment = CommentForm()
    return render(request, "post/home.html", {
        'posts': posts_data, 'form': comment})


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
    title = request.POST.get("title")
    description = request.POST.get("description")
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    up_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # we have two methods to save post creat() and save()
    Post.objects.create(
        title=title, description=description,
        publish_date=today_date, update_date=up_date,
        auther=request.user
        )
    # return redirect(add_post)
    ''' post_instance = Post(title=title,description=description,
        publish_date=today_date,update_date=up_date)'''
    # post_instance.save()


@permission_required('Wordoid.can_add_post', raise_exception=True)
def post_model_form(request):
    # user = User.objects.get(id=request.user.id)
    # if user.has_perm('Wordoid.can_add_post'):
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
    # return HttpResponse("you do not have permission to add post")


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
                "comment": post.post.values_list('text_field', flat=True)
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
        post_form = PostForm(request, instance=post)
    return render(
            request, "post/edit_post.html",
            {'form': post_form, 'obj': post}
            )


def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect(publish_post)


@csrf_exempt
def comment_post(request, id):
    post = Post.objects.get(id=id)
    parent_comment = post.post.filter(parent__isnull=True)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj

                instance = comment_form.save(commit=False)
                instance.post = post
                instance.user = request.user
                instance.save()
                print(replay_comment)
                reply_comment = Comment.objects.filter(id=replay_comment.id)
                prnt_obj = Comment.objects.filter(id=parent_obj.id)
                data = {
                    'lists': list(reply_comment.values()),
                    'parent_id': parent_id,
                    'parent_obj': list(prnt_obj.values()),
                    'message': 'reply successfully saved',
                    'status': 200
                    }
                return JsonResponse({'result': data})
            else:
                instance = comment_form.save(commit=False)
                instance.post = post
                instance.user = request.user
                instance.save()
                return redirect('read_more', post.id)
    # else:
    #     comment_form = CommentForm()
    # return render(request,
    #               'post/read_more.html',
    #               {'post': post,
    #                'comments': parent_comment,
    #                'comment_form': comment_form})


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
        'like_value': like_user,
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


def read_more(request, id):
    post = Post.objects.get(id=id)
    parent_comment = post.post.filter(parent__isnull=True)
    print(post.post.all())
    for item in Comment.objects.filter(parent__isnull=True):
        print(item.text_field)
        for child in item.replies.all():
            print(child.text_field)
            for child_of in child.replies.all():
                print(child_of.text_field)
    data = [{
            "id": post.id,
            "title": post.title,
            "description": post.description,
            "comments": post.post.all(),
            }]
    comment = CommentForm()
    return render(request, "post/read_more1.html", {
        'data': data,
        'form': comment,
        'nowcomment': parent_comment})
