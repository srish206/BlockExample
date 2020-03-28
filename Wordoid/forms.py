from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from Wordoid.models import Post
from Wordoid.models import Comment


class PostForm(forms.ModelForm):
	''' this method is use to get a request of user in a model form '''
	def __init__(self, request, *args, **kwargs):
		self.request = request
		super(PostForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Post
		# fields = '__all__'
		fields = ('title', 'description', 'publish')


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		# fields = ('post','text_field',)
		fields = ('text_field', )
		# labels = {
		# 	'text_field': ('write comment here'),
		# }
		# help_texts = {
		# 	'text_field': ('some usefull text'),
		# }

		# error_messages = {
		# 	'text_field': {
		# 		'min_length': ("This message is too short "),
		# 	},
		# }
