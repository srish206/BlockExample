from django.db import models
from django.contrib.auth.models import User
# from datetime import date
# import datetime


class UserProfile(models.Model):

    CHOICES = (
            ('R', 'reader'),
            ('A', 'author')
        )
    username = models.CharField(max_length=32)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=32 ,choices = CHOICES,default=False)
    password = models.CharField(max_length = 32,null = True, blank = True,verbose_name = 'password' )


    def __str__(self):
        return self.role


class Post(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    # publish_date = models.DateField(default=datetime.date.today)
    # update_date = models.DateField(default=datetime.date.today)
    publish_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    publish = models.BooleanField(default=False)
    liked_users = models.ManyToManyField(User)
    auther = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auther")

    class Meta:
        permissions = [
                ('can_add_post','can add a post'),
            ]


    @property
    def user_like(self):
        return self.liked_users.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post")
    text_field = models.TextField()
    like = models.IntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):          
        return '%s %s %s' %(self.user.username, self.post, self.text_field)


''' If the model field has blank=True, then required is set to False on the
        form field. Otherwise, required=True. '''
