
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
    
    recipeName = request.GET.get('search')
    sortType = request.GET.get('sorttype')
    
    dietTypeList = request.GET.getlist('diettype[]')  # jquery adds [] when sending through ajax
    categoryList = request.GET.getlist('categories[]')
    
    recipes = Recipe.objects.filter(name__contains=recipeName)
    
    #order after we have trun
    recipes = sortTypeDict.get(sortType,sortTypeDict['rating'])(recipes)
    # stops too many recipes being displayed on page
    if (len(recipes) >9 ):
        recipes =  recipes[:9]
    print(recipes)
    return recipes

