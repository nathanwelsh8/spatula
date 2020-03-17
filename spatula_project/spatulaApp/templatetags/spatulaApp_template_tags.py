from django import template 
from spatulaApp.models import Category, Recipe, Rating

register = template.Library() 

@register.filter
def getKeyImg(h,key):
    "Gets the image for display recipe on index page"
    for item in h:
        if item.belongsto.__str__() == key.__str__():
            return item.image

@register.filter
def getKeyImgList(h,key):
    "Get all images belonging to recipe object"
    images = []
    for item in h:
        if item.belongsto.__str__() == key.__str__():
            images.append(item.image)
    return images
    
@register.simple_tag
def double(a):
    return a*2

@register.filter
def getRating(redcipeID):
    ratings = Rating.objects.filter(recipe=redcipeID)
    rating = 0
    no_entries = 0
    for r in ratings:
        rating += r.rating
        no_entries +=1 
   
    return str(round((rating*2)/no_entries,0))