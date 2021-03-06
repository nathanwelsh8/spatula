from django import forms
from django.contrib.auth.models import User
from spatulaApp.models import UserProfile, Recipe, RecipeImage, Category, Rating, UserImage

from spatulaApp.customFormTypes import NameChoiceField

#choices for diettype field
DIET_CHOICES = Recipe.DIET_CHOICES # better to get from source than make a copy [(1,'Meat'), (2,'Vegan'), (3, 'Vegetarian'),]

#query Category table, add objects to tuple (ChoiceField requires tuple for choice perameter) 
class RecipeForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
         
        super(RecipeForm, self).__init__(*args, **kwargs)

    #input fields for recipe form
    method = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'placeholder':'Method - Please Take a new line for each step.'}))
    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder':'Recipe Name'}))
    ingredients = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'placeholder':'Ingredients - Please take a new line for each ingredient.'}))

    category = NameChoiceField(widget=forms.Select(), queryset =Category.objects.all(), initial = 0)

    toolsreq = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'placeholder':'Tools Required'}))
    difficulty = forms.ChoiceField(choices = ((1,'Basic'), (2,'Challenging'), (3, 'Difficult')), help_text = 'Difficulty: ')
    cost = forms.ChoiceField(choices = ((1, '£'), (2, '££'), (3, '£££')), help_text = 'Cost: ')
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
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={'placeholder': 'Username', 'id': 'register_username', 'class':'form-control'}),
                               label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'register_password','class':'form-control'}),
                               label='')

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserProfileForm(forms.ModelForm):
  
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Your bio - tell others about yourself...', 'id': 'bio', 'class':'form-control rounded-0'}), label='')

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

class ProfileImageUploadForm(forms.ModelForm):
    
    image = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control","id":'custom-file-input'}),required=False, label='Image')
    belongsto = forms.IntegerField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = UserImage
        fields = ('image',)

class UserProfileUpdateForm(forms.ModelForm):
    
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'You can update your bio if you please', 'id': 'bio'}), label='')
    
    class Meta:
        model = UserProfile
        fields = ('bio',)

class CommentForm(forms.ModelForm): 
    rating = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    comment = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'placeholder':'Comment'}))
    postedby = forms.SlugField(widget=forms.HiddenInput(),required=False)
    recipe = forms.SlugField(widget=forms.HiddenInput(),required=False)
    class Meta: 
        model = Rating
        fields = ('rating', 'comment')
