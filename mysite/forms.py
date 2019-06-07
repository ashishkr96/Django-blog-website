from django import forms
from .models import Profile, Comment, Post,About
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class AboutMe(forms.ModelForm):
    class Meta:
        model = About
        fields = ['about']


class Commentform(forms.ModelForm):
    content = forms.CharField(label='', max_length=160, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Text goes here', 'rows': '3', 'col': '2'}))

    class Meta:
        model = Comment
        fields = ['content']


class CreatePost(forms.ModelForm):
    content = forms.CharField(widget=TinyMCEWidget(attrs={'cols': 40, 'rows': 20}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'status']


