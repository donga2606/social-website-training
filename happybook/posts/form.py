from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    class Meta:
        model = Post
        fields = ('content', 'image')

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}),label='')
    class Meta:
        model = Comment
        fields = ('body', )
