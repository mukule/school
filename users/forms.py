from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    id_number = forms.CharField(
        label='ID Number',
        widget=forms.TextInput(attrs={'placeholder': 'ID Number', 'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
    )
