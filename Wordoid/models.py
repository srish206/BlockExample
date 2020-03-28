from django.db import models
from django.contrib.auth.models import User
from datetime import date
import datetime

# Create your models here.


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_auther = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

class Post(models.Model):
	title = models.CharField(max_length=20)
	description = models.TextField()
	# publish_date = models.DateField(default=datetime.date.today)
	# update_date = models.DateField(default=datetime.date.today)
	publish_date = models.DateField(auto_now_add=True)
	update_date = models.DateField(auto_now=True)
	publish = models.BooleanField(default=False)
	# like = models.IntegerField(default=0)
	liked_users = models.ManyToManyField(User)
	auther = models.ForeignKey(User,on_delete=models.CASCADE,related_name="auther")
	# user = models.ManyToManyField(User)

	@property
	def user_like(self):
		# import pdb;pdb.set_trace()
		return self.liked_users.count()
   

	def __str__(self):
		return self.title
#If the model field has blank=True, then required is set to False on the form field. Otherwise, required=True.

class Comment(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="post")
	text_field = models.TextField()
	like = models.IntegerField(default=0)

	def __str__(self):
		return self.user.username

	# def __str__(self):
	# 	return self.text_field

# class PostLike(models.Model):
# 	user = models.ForeignKey(User,on_delete=models.CASCADE)
# 	post = models.ForeignKey(Post,on_delete=models.CASCADE)

# 	def __str__(self):
# 		return '%s %s' % (self.user.username,self.post)