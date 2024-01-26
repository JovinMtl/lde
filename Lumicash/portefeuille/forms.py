
from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=15,\
                            widget=forms.TextInput(attrs={'value':'User'}))
    password = forms.CharField(widget=forms.PasswordInput())
