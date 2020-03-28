"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

#for aluth
from django.conf.urls import include
from Wordoid import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_page,name='home_page'),
    path('accounts/', include('allauth.urls'),name='accounts'),
    path('show-post',views.show_post,name='show_post'),
    path('change-post/<int:id>',views.change_post,name='change_post'),
    path('add-post',views.add_post,name='add_post'),
    path('add-post-form',views.post_model_form,name='add_post_form'),
    path('publish-post',views.publish_post,name='publish_post'),
    path('unpublish-post',views.unpublish_post,name='unpublish_post'),
    path('view-post/<int:id>',views.view_post,name='view_post'),
    path('edit-post/<int:id>',views.edit_post,name='edit_post'),
    path('delete_post/<int:id>',views.delete_post,name='delete_post'),
    path('comment-post/<int:id>',views.comment_post,name='comment_post'),
    path('like-post/<int:id>',views.like_post,name='like_post'),
    path('delete-comment/<int:id>',views.delete_comment,name='delete-comment'),
    path('search-data',views.search_data,name='search-data'),
]