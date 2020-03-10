from django import template 
from spatulaApp.models import Category

register = template.Library() 

@register.filter
def getKeyImg(h,key):
    for item in h:
        if item.belongsto.__str__() == key.__str__():
            return item.image
    
