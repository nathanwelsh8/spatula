
from spatulaApp.models import Recipe, RecipeImage, Rating
from django.db.models import Q
# Does not store actual views but instead stores 'queries'

def getRating(recipe,cache=None):
    'returns the rating for any given recipe if it exists'
    if not cache:
        cache = Rating.objects.all()
    total = 0
    num = 0
    for rating in cache.filter(recipe=recipe.id):
            total +=rating.rating
            num +=1
    if num <= 0:
       num =1
    #print(rating.recipe,num,total)
    return round(total/num,1) 
    

def sortRating(recipes):
    'Get all recipies --> get reviews for recipes --> sort in descending order --> return ordered recipes'

    rating_dict = {}
    rating_cache = Rating.objects.all()
    for recipe in recipes:
        # map recipe to its review value
        rating_dict[recipe] = getRating(recipe,rating_cache)
    
    # sorted() turns rating_dict into a tuple
    rating_dict = sorted(rating_dict.items(), key=lambda item: item[1], reverse=True) # get recipies from high to low
    
    for i in range(len(rating_dict)):
        x,r = rating_dict[i]
        rating_dict[i] = x
    return rating_dict
    

def sortPopularity(recipes):
    popularity_dict = {}
    rating_cache = Rating.objects.all()
    for recipe in recipes:
        num = rating_cache.filter(recipe=recipe.id).count()
        ratingVal = getRating(recipe, rating_cache) * num
        popularity_dict[recipe] = ratingVal 

    popularity_dict = sorted(popularity_dict.items(), key=lambda item: item[1], reverse=True) # get recipies from high to low

    for i in range(len(popularity_dict)):
        x,r = popularity_dict[i]
        popularity_dict[i] = x
    return popularity_dict

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
