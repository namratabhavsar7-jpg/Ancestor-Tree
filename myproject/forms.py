from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class ProfessionalRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'auth-input'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'auth-input'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'auth-input'
    }))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'placeholder': 'Phone Number',
        'class': 'auth-input'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        return user

class ProfessionalLoginForm(forms.Form):
    login_id = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username or Email Address',
        'class': 'auth-input'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'auth-input'
    }))
