from dataclasses import field
from pyexpat import model
from django import forms
from .models import Comment, Post

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields= ('name', 'email', 'body')

class Addpost(forms.ModelForm):
    class Meta:
        model= Post
        fields= ['title','slug','author','body', 'publish','status','tags']