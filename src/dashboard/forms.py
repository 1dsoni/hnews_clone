from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'password1', 'password2', )

class LoginForm(forms.Form):
    email = forms.EmailField(label='Your email', max_length=100)
    password = forms.CharField(label='Your password', max_length=100)

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label='Your email', max_length=100)
