from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True, label='شماره تماس')
    email = forms.EmailField(required=False, label='ایمیل')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password1', 'password2')