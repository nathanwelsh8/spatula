from django import forms
from django.contrib.auth.models import User
from spatulaApp.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Fields list empty since we don't want the profile fields to appear during registration
        fields = ()
