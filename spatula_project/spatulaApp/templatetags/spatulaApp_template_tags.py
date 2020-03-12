from django import template 
from spatulaApp.models import Category

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
    
