import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'spatula_project.settings')

import django

django.setup()

from spatulaApp.models import Category
from spatulaApp.models import Recipe
from django.contrib.auth.models import User
from spatulaApp.models import UserProfile
from spatulaApp.models import Rating


def populate():
    users = [
        {'username': 'bob777', 'password': '123', 'bio': 'Hi Im bob and i like cooking'},
        {'username': 'crazyman4', 'password': '222', 'bio': 'I like cooking and getting crazy'},
    ]

    categories = [
        {'name': 'Italian'},
        {'name': 'Chinese'},
        {'name': 'Thai'},
        {'name':'Japanese'},
        {'name': 'Western'},
        {'name': 'Indian'},
        {'name': 'Mexican'},
        {'name': 'Other'}
    ]

     # you need to pass the user object to the model not the string name.
     # otherwise bobs profile page wont be able to find his recipies 
    

    print("Adding Users:")
    for user in users:
        u = add_user(user)
        print("\t Added", u)

    print("Adding Categories:")
    for cat in categories:
        c = add_category(cat)
        print("\t Added", c)

    bob = UserProfile.objects.get(user=User.objects.get(username='bob777'))
    recipies = {
        'Vegetable Stir Fry':
        {
            'ingredients': '2 tbsp sunflower oil, 4 spring onions, 1 garlic clove, piece fresh root ginger, 1 carrot, 1 red pepper, 100g/3oz baby sweetcorn, 1 courgette, 150g/5oz sugar-snap peas, 2 tbsp hoisin sauce, 2 tbsp low-salt soy sauce',
            'toolsreq': 'Wok, Spatula',
            'method': 'Heat a wok on a high heat and add the sunflower oil. Add the spring onions, garlic, ginger and stir-fry for 1 minute, then reduce the heat. Take care to not brown the vegetables. /ES        Add the carrot, red pepper and baby sweetcorn and stir-fry for 2 minutes. Add the courgette and sugar snap peas and stir-fry for a further 3 minutes. Toss the ingredients from the centre to the side of the wok using a wooden spatula. Do not overcrowd the wok and keep the ingredients moving. /ES Add 1 tablespoon water, hoisin and soy sauce and cook over a high heat for a further 2 minutes or until all the vegetables are cooked but not too soft. Serve with noodles or rice. /ES',
            'difficulty': 1,
            'cost': 1,
            'diettype': 3,
            'rating': 3,
            'category': 'Chinese',
            'postedby': bob
        },
        'American Style Burger':
        {
            'ingredients': 'Mince, Herbs, Buns, Eggs, Seasioning, Cheese',
            'toolsreq': 'Frying pan',
            'method': 'Fry burgers',
            'difficulty': 3,
            'cost': 2,
            'diettype': 1,
            'rating': 1,
            'category': 'Western',
            'postedby': bob
        }
    }

    print("Adding Recipes:")
    for recipe, recipe_data in recipies.items():
        r = add_recipe(recipe, recipe_data)
        print("\t Added", r)

    # you need to pass the object to the model not the string name.
    vsf = Recipe.objects.filter(name='Vegetable Stir Fry')[0]
    asb = Recipe.objects.filter(name='American Style Burger')[0]
    ratings = [
        {'recipe': vsf, 'rating': 5},
        {'recipe': vsf, 'rating': 3},
        {'recipe': asb, 'rating': 4},
        {'recipe': asb, 'rating': 4},
        {'recipe': asb, 'rating': 5},
        {'recipe': asb, 'rating': 3},
        {'recipe': asb, 'rating': 4},
        {'recipe': asb, 'rating': 4},
        {'recipe': asb, 'rating': 5},
        {'recipe': asb, 'rating': 3},
        {'recipe': asb, 'rating': 1},
        {'recipe': asb, 'rating': 4},
    ]
    print("Adding Ratings")
    for rating in ratings:
        add_rating(rating)

def add_user(user_info):
    new_user = User.objects.get_or_create(username=user_info['username'], password=user_info['password'])[0]
    profile = UserProfile.objects.get_or_create(user=new_user, bio=user_info['bio'])[0]
    new_user.save()
    profile.save()
    return user_info['username']


def add_category(category_dict):
    c = Category.objects.get_or_create(name=category_dict['name'])[0]
    c.save()
    return category_dict['name']


def add_recipe(name, recipe_data):
    postedby_user = User.objects.get_or_create(username=recipe_data['postedby'])[0]
    postedby_user_profile = UserProfile.objects.get_or_create(user=postedby_user)[0]
    category = Category.objects.get_or_create(name=recipe_data['category'])[0]

    r = Recipe.objects.get_or_create(name=name, ingredients=recipe_data.get('ingredients'),
                                     toolsreq=recipe_data.get('toolsreq'), method=recipe_data.get('method'),
                                     difficulty=recipe_data.get('difficulty'), cost=recipe_data.get('cost'),
                                     diettype=recipe_data.get('diettype'), rating=recipe_data.get('rating'),
                                     postedby=postedby_user_profile, category=category)[0]
    r.save()
    return r


def add_rating(rating_info):
    # careful we can have more than one recipe with this name, use filter
    recipe = Recipe.objects.filter(name=rating_info['recipe'])[0]
    r = Rating(recipe=recipe, rating=rating_info['rating'])
    r.save()

if __name__ == '__main__':
    print("Populating database...")
    populate()
    print("Population complete")