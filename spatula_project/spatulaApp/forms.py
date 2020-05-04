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
    method = forms.CharField(max_length=2**13, widget=forms.Textarea(attrs={'placeholder':'Method - Please Take a new line for each step. Other users are morelikely to read your recipe this way.','class':'form-control','autocomplete':'off'}))
    name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder':'Something delicious, that will grab users attention','class':'form-control','autocomplete':'off'}))
    ingredients = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'placeholder':'Ingredients - Please take a new line for each ingredient. Users will find it easier to read.',
        'class':'form-control','autocomplete':'off'}))

    category = NameChoiceField(widget=forms.Select(), queryset =Category.objects.all(), initial = 0)

    toolsreq = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'placeholder':'Tools Required','autocomplete':'off'}))
    difficulty = forms.ChoiceField(choices = ((1,'Easy'), (2,'Challenging'), (3, 'Technical')), help_text = 'Difficulty: ')
    cost = forms.ChoiceField(choices = ((1, '£'), (2, '££'), (3, '£££')), help_text = 'Cost: ')
    diettype = forms.IntegerField(widget=forms.RadioSelect(choices=DIET_CHOICES))
    cooktime = forms.ChoiceField(choices=Recipe.COOKTIME_CHOICES, help_text="Time to cook (Approx):", widget=forms.Select(attrs={'class':'form-control'}))
    portionsize = forms.ChoiceField(choices=Recipe.PORTION_SIZES, help_text="Portion size:", widget=forms.Select(attrs={'class':'form-control'}))
    # not required as its not stored in DB
    description = forms.CharField(max_length=64,widget=forms.Textarea(attrs={'placeholder':'A short description to summarise your recipe','autocomplete':'off','class':'form-control'}))
    
    
    #hidden fields
    rating = forms.FloatField(widget=forms.HiddenInput(), initial=0, required=False)
    slug = forms.SlugField(widget=forms.HiddenInput(),required=False)
    postedby = forms.SlugField(widget=forms.HiddenInput(),required=False)
    
    #Order in which inputs get rendered
    field_order = ['name', 'category', 'toolsreq', 'difficulty', 'cost', 'diettype', 'cooktime', 'portionsize' , 'ingredients', 'method']
   
    class Meta: 
        model = Recipe
        exclude = ('id','postedby')
    



class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Username',
                                    'id': 'register_username',
                                    'class':'form-control',
                                    'autocomplete':'off',
                                    }),
                               label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'register_password','class':'form-control'}),
                               label='')
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder':'i-love-cooking@gmail.com',
        'id':'register_email',
        'class':'form-control',
        'autocomplete':'off',
        }),
         label='')

    class Meta:
        model = User
        fields = ('username', 'password','email',)


class UserProfileForm(forms.ModelForm):
  
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Your bio - tell others about yourself...',
         'id': 'bio',
         'class':'form-control rounded-0',
         'autocomplete':'off',
         'value':'&#8;'}),
         label='')

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
