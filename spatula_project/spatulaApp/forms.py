from django import forms
from django.contrib.auth.models import User
from spatulaApp.models import UserProfile, Recipe, Category

#choices for diettype field
DIET_CHOICES = [(1,'Meat'), (2,'Vegan'), (3, 'Vegetarian'),]

#query Category table, add objects to tuple (ChoiceField requires tuple for choice perameter) 

class RecipeForm(forms.ModelForm):
    
    #input fields for recipe form
    method = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'placeholder':'Method'}))
    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder':'Recipe Name'}))
    ingredients = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'placeholder':'Ingredients'}))
    category = forms.ChoiceField(widget=forms.Select(), choices = "")
    toolsreq = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'placeholder':'Tools Required'}))
    difficulty = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'step':'1', 'min':'1','max':'3'}), help_text = 'Difficulty: ')
    cost = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'step':'1', 'min':'1','max':'3'}), help_text = 'Cost: ')
    diettype = forms.IntegerField(widget=forms.RadioSelect(choices=DIET_CHOICES))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description'}))
    
    
    #hidden fields
    rating = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    slug = forms.SlugField(widget=forms.HiddenInput())
    postedby = forms.SlugField(widget=forms.HiddenInput())
    
    #Order in which inputs get rendered
    field_order = ['name', 'category', 'toolsreq', 'description', 'difficulty', 'cost', 'diettype', 'ingredients', 'method']
   
    class Meta: 
        model = Recipe
        exclude = ('id',)


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':'Username'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}), label='')

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Your bio - tell us about yourself...'}), label ='')

    class Meta:
        model = UserProfile
        # Fields list empty since we don't want the profile fields to appear during registration
        exclude = ('user', 'slug')
