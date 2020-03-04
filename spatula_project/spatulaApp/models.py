from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth.models import User
import os
# Create your models here.

NAME_MAX_LENGTH = 128
MAX_TEXT_LENGTH = 512

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

    name            = models.CharField(max_length=NAME_MAX_LENGTH)
    ingredients     = models.TextField(max_length=MAX_TEXT_LENGTH)
    
    toolsreq        = models.TextField(max_length=MAX_TEXT_LENGTH)
    method          = models.TextField()
    # make sure the form views for difficulty, 
    # cost and diettype datatypes restrict the 
    # users selection to the CHOICES above
    difficulty      = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES, max_digits=1)
    cost            = models.PositiveSmallIntegerField(choices=COST_CHOICES, max_digits=1)
    diettype        = models.PositiveSmallIntegerField(choices=DIET_CHOICES ,max_digits=1)
   
    #image           = 
    #postedby        = 

    # Following fields are hidden when creating a new recipe
    #ratings are out of 5, to 1 decimal place
    rating          = models.DecimalField(decimal_places=1,max_digits=3, default=0)
    slug            = models.Slugfield(unique=True)
    category        = models.ForeignKey(Recipe,to_field="name", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        self.slug = slugify(str(self.name)+str(self.id))
        super(Category,self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=25)


class UserProfile(models.Model):
    pass


class Image(models.Model):

    def images_path():
        return os.path.join(settings.IMAGES_DIR, 'images')

    image = models.FilePathField(path=images_path)

class Rating(models.Model):

    #auto filled by form so not shown to user 
    recipe     = models.ForeignKey(Recipe)
    #user   = models.ForeignKey(Recipe, to_field="poastedBy")
    
    # editable by user
    rating     = models.PositiveSmallIntegerField(decimal_places=2, max_digits=3, default=0)
    
    # comments are optional
    comment    = models.TextField(max_length=MAX_TEXT_LENGTH, required=False)