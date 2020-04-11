from django import forms
from Wordoid.models import Post
from Wordoid.models import Comment
# from Wordoid.validators import validate_text


class PostForm(forms.ModelForm):
    ''' this method is use to get a request of user in a model form '''

    title = forms.CharField(
        label='Post Title',
        widget=forms.TextInput(attrs={
            'placeholder': 'Title',
            'size': 20,
        }))
    description = forms.CharField(
        widget=forms.Textarea(
                attrs={'placeholder': 'write description here', 'size': 50}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(PostForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        # fields = '__all__'
        fields = ('title', 'description', 'publish')

    # def clean(self):
    #     cleaned_data = super().clean()
    #     title = cleaned_data.get('title')
    #     # title = self.cleaned_data['title']
    #     if Post.objects.filter(title=title):
    #         raise forms.ValidationError('Post with this title already exists.')


class CommentForm(forms.ModelForm):
    # text_field = forms.CharField(widget=forms.Textarea,validators=[validate_text])
    text_field = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'write comment here'})
        )

    class Meta:
        model = Comment
        # fields = ('post','text_field',)
        fields = ('text_field', )
        # labels = {
        #   'text_field': ('write comment here'),
        # }
        # help_texts = {
        #   'text_field': ('some usefull text'),
        # }

        # error_messages = {
        #   'text_field': {
        #       'min_length': ("This message is too short "),
        #   },
        # }
