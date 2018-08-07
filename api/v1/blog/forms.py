from django import forms
from blog.models import Comment


class CommentForm(forms.ModelForm):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    content = forms.CharField(label='', widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
