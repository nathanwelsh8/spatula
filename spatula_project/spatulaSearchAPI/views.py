
from spatulaApp.models import Recipe, RecipeImage
from django.db.models import Q
# Does not store actual views but instead stores 'queries'

def sortRating(recipes):
    return recipes

def sortPopularity(recipes):
    return recipes

def sortDifficulty(recipes):
    return recipes.order_by('difficulty')

def sortCost(recipes):
    return recipes.order_by('cost')

sortTypeDict = {'rating':sortRating,'cost':sortCost,'difficulty':sortDifficulty,'popularity':sortPopularity}
def search(request):
    
    # provide alternative value incase the user 
    # attempts to submit bogus data to server
    recipeName = request.GET.get('search','chicken')
    sortType = request.GET.get('sorttype','popularity')
    dietTypeList = request.GET.getlist('diettype[]',[1])  # jquery adds [] when sending lists through ajax
    categoryList = request.GET.getlist('categories[]','Italian')
   
    recipes = Recipe.objects.filter(Q(name__contains=recipeName) & Q(category__in=categoryList) & Q(diettype__in=dietTypeList))
    
    # sort the results as per users request
    recipes = sortTypeDict.get(sortType,sortTypeDict['rating'])(recipes)
    # stops too many recipes being displayed on page
    if (len(recipes) >9 ):
        recipes =  recipes[:9]
    return recipes
