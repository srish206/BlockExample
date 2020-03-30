from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_paginated_objects(request, user_post):
    page = request.GET.get('page', 1)
    paginator = Paginator(user_post, settings.PAGE_COUNT)
    try:
        user_post = paginator.page(page)
    except PageNotAnInteger:
        user_post = paginator.page(1)
    except EmptyPage:
        user_post = paginator.page(paginator.num_pages)
    return user_post
