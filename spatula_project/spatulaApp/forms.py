from django import forms
from django.contrib.auth.models import User
from spatulaApp.models import UserProfile, Recipe, Category, RecipeImage
from spatulaApp.customFormTypes import NameChoiceField

#choices for diettype field
DIET_CHOICES = Recipe.DIET_CHOICES # better to get from source than make a copy [(1,'Meat'), (2,'Vegan'), (3, 'Vegetarian'),]
CATEGORY_CHOICES = [(choice.name,choice.name) for choice in Category.objects.all()]
#query Category table, add objects to tuple (ChoiceField requires tuple for choice perameter) 
class RecipeForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
         
        super(RecipeForm, self).__init__(*args, **kwargs)

    #input fields for recipe form
    method = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'placeholder':'Method'}))
    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder':'Recipe Name'}))
    ingredients = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'placeholder':'Ingredients'}))

    category = NameChoiceField(widget=forms.Select(), queryset =Category.objects.all(), initial = 0)

    toolsreq = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'placeholder':'Tools Required'}))
    difficulty = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'step':'1', 'min':'1','max':'3'}), help_text = 'Difficulty: ')
    cost = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'step':'1', 'min':'1','max':'3'}), help_text = 'Cost: ')
    diettype = forms.IntegerField(widget=forms.RadioSelect(choices=DIET_CHOICES))

    # not required as its not stored in DB
    #description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description'})) 
    
    
    #hidden fields
    rating = forms.FloatField(widget=forms.HiddenInput(), initial=0, required=False)
    slug = forms.SlugField(widget=forms.HiddenInput(),required=False)
    postedby = forms.SlugField(widget=forms.HiddenInput(),required=False)
    
    #Order in which inputs get rendered
    field_order = ['name', 'category', 'toolsreq', 'difficulty', 'cost', 'diettype', 'ingredients', 'method']
   
    class Meta: 
        model = Recipe
        exclude = ('id','postedby')
    




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

class RecipeImageUploadForm(forms.ModelForm):
    
    image = forms.ImageField(required = False, label='Image')
    belongsto = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = RecipeImage
        fields = ('image',)