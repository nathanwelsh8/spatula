from django import forms
from django.contrib.auth.models import User
from spatulaApp.models import UserProfile, Recipe, Category, RecipeImage

class SearchForm(forms.Form):
    recipeName = forms.CharField(max_length=25)
    
