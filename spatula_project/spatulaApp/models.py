from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth.models import User
import os
import PIL.Image
# Create your models here.

NAME_MAX_LENGTH = 128
MAX_TEXT_LENGTH = 512


class UserProfile(models.Model):
    # This is the same implementation as the TWDjango, 
    # so look there when building the login forms
    # Default usermodel has name, username, and password 
    # fields. We can just use what we need. 

    
    user      = models.OneToOneField(User, on_delete=models.CASCADE)
    
    bio  = models.TextField(blank=True)   
    slug            = models.SlugField(unique=True, blank=True)

    # profile_pic = models.OneToOneField(Image)

    # users rating is calculated live when userinfo requested.
    # no user rating to be stored

    def __str__(self):
        return self.user.username
    
    # username slug is used for the URL name mappings
    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.__str__()))
        super(UserProfile,self).save(*args,**kwargs)

class Category(models.Model):
    
    # In a 1:N with Recipe. Recipe table points to here.

    name = models.CharField(primary_key=True, unique=True, max_length=25)

    def getModelsAsList():
        return Category.objects.values_list('name',flat=True)

class Recipe(models.Model):
  
    DIET_CHOICES = (
                (1,"Meat"),
                (2,"Vegetarian"),
                (3,"Vegan"),
    )
    DIFFICULTY_CHOICES   = (
                (1,1),
                (2,2),
                (3,3),
    )
    COST_CHOICES        = (
                (1,1),
                (2,2),
                (3,3),
    )

    name                   = models.CharField(max_length=NAME_MAX_LENGTH)
    ingredients            = models.TextField(max_length=MAX_TEXT_LENGTH)
    toolsreq               = models.TextField(max_length=MAX_TEXT_LENGTH)
    method                 = models.TextField()

    # make sure the form views for difficulty, 
    # cost and diettype datatypes restrict the 
    # users selection to the CHOICES above
    difficulty             = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES)
    cost                   = models.PositiveSmallIntegerField(choices=COST_CHOICES)
    diettype               = models.PositiveSmallIntegerField(choices=DIET_CHOICES)
   
    postedby               = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=0)

    #  - Following fields are hidden when creating a new recipe
    #       ratings are out of 5, to 1 decimal place.
    #  - Need a script to update rating everytime
    #       a new rating for the recipe is posted.
    rating                 = models.DecimalField(decimal_places=1,max_digits=3, default=0)
    category               = models.ForeignKey(Category,to_field="name", on_delete=models.CASCADE)

    # recipes rating is calculated when the recipe is requested, no value to be stored

    def __str__(self):
        return self.name

    def getChoicesAsList():
        l = []
        for c in Recipe.DIET_CHOICES:
            l.append([c[0],c[1]])
        return l 
    
    def getRecipiesAsDict():
        recipe_query = Category.objects.values()
        repice_dict = {} 
   
    
    # used for recipe mappings
    def save(self,*args, **kwargs):
        self.slug = slugify(str(self.name)+str(self.postedby))
        super(Recipe,self).save(*args, **kwargs)


class Image(models.Model):

    # this might work?
    def images_path():
        return os.path.join(settings.IMAGES_DIR, 'usruploads')

    def resize(self):
        im = PIL.Image.open(self.image)
        size=(200,200)
        out = im.resize(size)
        out.save(self.image.__str__())

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)
        self.resize()

    #image      = models.FilePathField(path=images_path)
    # Django docs are using image 
    # field instead of FilePathField
    # so try this first

    image      = models.ImageField(upload_to=images_path()[1:], max_length=255)

class UserImage(Image):
    belongsto = models.ForeignKey(UserProfile,  on_delete=models.CASCADE)

    

class RecipeImage(Image):
    belongsto = models.ForeignKey(Recipe,  on_delete=models.CASCADE)

    
class Rating(models.Model):

    #auto filled by form so not shown to user 
    recipe     = models.ForeignKey(Recipe, related_name="belongs_to", on_delete=models.CASCADE)
    
    ### editable by user ###
    rating     = models.DecimalField(decimal_places=2, max_digits=3, default=0)
    # comments are optional
    comment    = models.TextField(max_length=MAX_TEXT_LENGTH, blank=True)