from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.

class Recipe(models.Model):

    NAME_MAX_LENGTH = 128
    MAX_TEXT_LENGTH = 512
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
    
    # make sure the form views for difficulty, 
    # cost and diettype datatypes restrict the 
    # users selection to the CHOICES above
    difficulty      = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES, max_digits=1)
    cost            = models.PositiveSmallIntegerField(choices=COST_CHOICES, max_digits=1)
    diettype        = models.PositiveSmallIntegerField(choices=DIET_CHOICES ,max_digits=1)
   
    #image           = 
    #postedby        = 
    #ratings are out of 5, to 1 decimal place
    rating          = models.DecimalField(decimal_places=1,max_digits=3)
    slug            = models.Slugfield(unique=True)
    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        self.slug = slugify(str(self.name)+str(self.id))
        super(Category,self).save(*args, **kwargs)


class Category(models.Model):
    pass

class UserProfile(models.Model):
    pass

class Image(models.Model):
    pass
class Rating(models.Model):
    pass