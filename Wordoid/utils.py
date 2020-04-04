from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_paginated_objects(request, items):
    page = request.GET.get('page', 1)
    paginator = Paginator(items, settings.PAGE_COUNT)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items
