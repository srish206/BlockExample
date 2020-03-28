from django import template
from Wordoid.models import Post
from Wordoid.models import Comment

register = template.Library()


@register.filter(name='get_comment_post')
def get_comment_post(arg):
	# posts = Post.objects.all()
	# comment_list = []
	# for post in posts:
	# 	# import pdb;pdb.set_trace()
	# 	for comment in post.post.all():
	# 		comment_list.append(comment.text_field)

	# # for post in posts:
	# # 	comment_list.append({
	# # 			'comment':post.post.values_list('text_field')
	# # 		})
		
	# return comment_list

	posts = Post.objects.all()
	post_comment = []
	for post in posts:
		post_comment.append({
				"title": post.title,
				"auther": post.auther,
				"description": post.description,
				# "comment": post.post.all()
				"comment":list(post.post.values_list('text_field'))
			})
	return post_comment