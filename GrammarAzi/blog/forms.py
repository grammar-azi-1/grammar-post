from django import forms
from blog.models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'userId',
            'image',
            'content'
        )
        widgets = {
            'content': forms.Textarea(attrs= {
                'placeholder': 'Content *'
            }),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = (
            'parentCommentId',
            'userId',
            'postId',
            'content',
            'image',
        )
        widgets = {
            'content': forms.Textarea(attrs= {
                'placeholder': 'Content *'
            }),
        }