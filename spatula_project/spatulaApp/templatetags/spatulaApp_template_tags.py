from django import template 
from spatulaApp.models import Category, Recipe, Rating, UserProfile, UserImage
from django.contrib.auth.models import User
from math import sqrt, log
register = template.Library() 

@register.filter
def getKeyImg(h,key):
    "Gets the image for display recipe on index page"
    if h is None:
        return defaultImage()
    try:
        if type(h) == list:
            for i in h:
                for j in i:
                    if j is None:
                        pass
                    if j.belongsto.__str__() == key.__str__():
                        return j.image
        
        for item in h:
            if item is None:
                pass 
            if item.belongsto.__str__() == key.__str__():
                return item.image
    except AttributeError:
        return defaultImage()

        
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

@register.filter
def getProfileRating(username):

    # Users rating is based an weighted averge of all their recipies ratings
    # it is wighted such that the rating is biased agaisnt the number of reviews
    # calculated using y=|ln(sqrt(Rn+1))*5| , y<R, R=avergae rating, n=no.ratings

    try:
        user = UserProfile.objects.get(user=User.objects.get(username=username))
        recipies = Recipe.objects.filter(postedby=user.id)

        total = 0
        length = len(recipies)
        for recipie in recipies:
            total += int(getRating(recipie.id)) 
        
        if length==0:
            length = 1

        average = total/length

        weightedAverage = log(abs(sqrt(average+1)))*5
        if weightedAverage > average:
            weightedAverage = average

        return str(round(weightedAverage*2,0)/2)     

    except UserProfile.DoesNotExist:
        return str(0)
    except User.DoesNotExist:
        return str(0)

@register.filter
def getNumRecipies(username):
    try:
        user = UserProfile.objects.get(user=User.objects.get(username=username))
        recipies = Recipe.objects.filter(postedby=user.id)
        return str(len(recipies))
    except Exception:
        return str(0)
        


@register.filter
def getProfilePicture(user):
    try:
        #handle object requests
        user_image = UserImage.objects.filter(belongsto=user)
        if len(user_image) == 0:
            raise IndexError("user does not have profile pic")
        return user_image[0].image
        
    except ValueError:
        #handle string requests
        user_image = UserImage.objects.filter(belongsto=UserProfile.objects.get(user=User.objects.get(username=user)))
        if len(user_image) == 0:
            return defaultImage()
        return user_image[0].image
    except UserImage.DoesNotExist:
        return defaultImage()
    except User.DoesNotExist:
        return defaultImage()
    except UserProfile.DoesNotExist:
        return defaultImage()
    except IndexError as err:
        return defaultImage()
    

def defaultImage():
    return UserImage.objects.get(belongsto=UserProfile.objects.get(user=User.objects.get(username="default_user"))).image

    

