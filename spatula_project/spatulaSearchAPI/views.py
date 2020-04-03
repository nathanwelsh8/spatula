
from spatulaApp.models import Recipe, RecipeImage, Rating, Category
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

# must go after the functions it stores
sortTypeDict = { 'rating':sortRating, 
                'cost':sortCost,
                'difficulty':sortDifficulty,
                'popularity':sortPopularity
                }


def search(request, user_filter=None, cache=None):
    """
    Search recipies, request can contain the following keys:
        search: the text to search by
        sorttype: one of ["rating","popularity","cost","difficulty"]
        diettype: a list of accepted diet types [1,2,3] see Recipe model for what each integer represents
        categories: a list of accpeted categories to search by
    
    user_filter is the ID of the user object to filter by default is None, which does not refine by user.
    
    Returns no more than 9 recipies at a time to stop page from being swamped
    Returns a list of Recipe objects to inject into the results.html template
    """

    # provide alternative values incase the request only submits 
    # a search text. in this case assume that they want to refine
    # only by text and leave everything else unrefined
    recipeName = request.GET.get('search','')
    sortType = request.GET.get('sorttype','popularity')
    dietTypeList = request.GET.getlist('diettype[]',[1,2,3])  # jquery adds [] when sending lists through ajax
    categoryList = request.GET.getlist('categories[]', [str(x.name) for x in Category.objects.all()]) # not many categorys so no need to cache
    
    # all vegan food is vegetarian so include both 
    # vegetarian and vegan food when vegan selected
    
    if dietTypeList == ['3']:
        print(dietTypeList == ['3'])
        dietTypeList = [2,3]
    print(dietTypeList)
    
    return core(recipeName=recipeName,sortType=sortType,dietTypeList=dietTypeList,categoryList=categoryList,user_filter=user_filter,cache=cache)

def non_http_search(request, user_filter=None,cache=None):
    recipeName = request.get('search')
    return core(recipeName=recipeName)
    
try: 
    cat_list = [str(x.name) for x in Category.objects.all()]
except Exception:
    cat_list = None

def core(
    recipeName='',
    sortType='popularity',
    dietTypeList=[1,2,3],
    categoryList=cat_list, 
        
    user_filter=None,
    cache=None
      ):
    
    if cache:
        recipes = cache.filter(Q(name__contains=recipeName) & Q(category__in=categoryList) & Q(diettype__in=dietTypeList))
    else:
        recipes = Recipe.objects.filter(Q(name__contains=recipeName) & Q(category__in=categoryList) & Q(diettype__in=dietTypeList))
    
    if user_filter:
        recipes = recipes.filter(postedby=user_filter)
    # sort the results as per users request
    recipes = sortTypeDict.get(sortType,sortTypeDict['rating'])(recipes)
    # stops too many recipes being displayed on page
    if (len(recipes) >9 ):
        recipes =  recipes[:9]
    return recipes