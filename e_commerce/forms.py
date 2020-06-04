from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    """Form for regisger"""
    username = forms.CharField(max_length=50,
                               min_length=4,
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'id': 'username',
                                   'placeholder': 'username'
                               }))
    email = forms.EmailField(required=True,
                               widget=forms.EmailInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'example@email.com'
                               }))
    password = forms.CharField(required=True,
                               min_length=4,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'password'
                               }))

    password2 = forms.CharField(required=True,
                               min_length=4,
                               label='Confirm password',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Confirm password'
                               }))


    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('User already exist')

        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already is in use')

        return email


    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password') != cleaned_data.get('password2'):
            self.add_error('password2', 'The password do not match')


    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
            )
