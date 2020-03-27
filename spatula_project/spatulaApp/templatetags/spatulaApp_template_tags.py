from django import template 
from spatulaApp.models import Category, Recipe, Rating

register = template.Library() 

@register.filter
def getKeyImg(h,key):
    "Gets the image for display recipe on index page"
    try:
        if type(h) == list:
            for i in h:
                for j in i:
                    if j.belongsto.__str__() == key.__str__():
                        return j.image
            
        for item in h:
            if item.belongsto.__str__() == key.__str__():
                return item.image
    except AttributeError:
        return None

    

        
@register.filter
def getKeyImgList(h,key):
    "Get all images belonging to recipe object"
    images = []
    
    for item in h:
        if item.belongsto.__str__() == key.__str__():
            images.append(item.image)
    return images

@register.filter
def getReviews(h, key): 
    reviews = []
    
    for item in h: 
        if item.recipe.__str__() ==key.__str__(): 
            item.rating = str(round((int(item.rating)*2)))
            reviews.append(item)
    return reviews
    
@register.simple_tag
def double(a):
    return a*2

@register.filter
def getRating(recipeID):
    ratings = Rating.objects.filter(recipe=recipeID)
    rating = 0
    no_entries = 0
    for r in ratings:
        rating += r.rating
        no_entries +=1 


    # bad idea to divide by zero    
    if no_entries == 0:
        no_entries = 1
    return str(round((rating*2)/no_entries))


@register.filter
def getNoRatings(recipeID):
    return Rating.objects.filter(recipe=recipeID).count()
    
@register.filter
def recipeNameLengthCheck(name):
    if len(str(name))>21:
        name = name[:19]+"..."
    return name