from django import forms
from .models import BlogPost, Comment
from ckeditor.widgets import CKEditorWidget


class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # Removed config_name

    class Meta:
        model = BlogPost
        fields = ["title", "content", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a comment...'
            }),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Write a reply...'
            }),
        }
