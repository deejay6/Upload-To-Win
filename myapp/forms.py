from django import forms
from models import User, PostModel


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'age',  'phone', 'email', 'password', 'gender']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=100)

    class Meta:
        fields = ['username', 'password']


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['image', 'caption']