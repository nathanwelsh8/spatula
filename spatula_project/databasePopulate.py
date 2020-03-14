import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'spatula_project.settings')

import django
django.setup()

from spatulaApp.models import Category
from spatulaApp.models import Recipe


def populate():    

    categories = [
        {
            'name':'Italian',

        },
        {
            'name':'Chinese'
        },
        {
            'name':'Thai'
        },
        {
            'name':'Western'
        },
        {
            'name':'Indian'
        },
        {
            'name':'Mexican'
        },
        {
            'name':'Other'
        }
    ]
    
    recipies = {'Vegtable Stir Fry':
                                    {
                                        'ingredients':'2 tbsp sunflower oil, 4 spring onions, 1 garlic clove, piece fresh root ginger, 1 carrot, 1 red pepper, 100g/3oz baby sweetcorn, 1 courgette, 150g/5oz sugar-snap peas, 2 tbsp hoisin sauce, 2 tbsp low-salt soy sauce',
                                        'toolsreq':'Wok, Spatula',
                                        'method': 'Heat a wok on a high heat and add the sunflower oil. Add the spring onions, garlic, ginger and stir-fry for 1 minute, then reduce the heat. Take care to not brown the vegetables. /ES        Add the carrot, red pepper and baby sweetcorn and stir-fry for 2 minutes. Add the courgette and sugar snap peas and stir-fry for a further 3 minutes. Toss the ingredients from the centre to the side of the wok using a wooden spatula. Do not overcrowd the wok and keep the ingredients moving. /ES Add 1 tablespoon water, hoisin and soy sauce and cook over a high heat for a further 2 minutes or until all the vegetables are cooked but not too soft. Serve with noodles or rice. /ES',
                                        'difficulty':1,
                                        'cost':1,
                                        'diettype':3,
                                        'rating':3,
                                        'category':'Chinese',
                                    }
                , 'American Style Burger':
                                    {
                                        'ingredients':'Mince, Herbs, Buns, Eggs, Seasioning, Cheese',
                                        'toolsreq':'Frying pan',
                                        'method':'Fry burgers',
                                        'difficulty':3,
                                        'cost':2,
                                        'diettype':1,
                                        'rating':1,
                                        'category':'Other',
                                    }
                }  
    

    for cat in categories:
        c = add_category(cat)
        print("\t Added",c)

    for recipe, recipe_data in recipies.items(): 
        r = add_recipe(recipe, recipe_data)
        print("\t Added",r)
    


def add_category(category_dict):
    c = Category.objects.get_or_create(name=category_dict['name'])[0]
    c.save()
    return c

def add_recipe(name, recipe_data): 
    r = Recipe.objects.get_or_create(name=name, ingredients=recipe_data.get('ingredients'), toolsreq=recipe_data.get('toolsreq'), method=recipe_data.get('method'), difficulty=recipe_data.get('difficulty'), cost=recipe_data.get('cost'), diettype=recipe_data.get('diettype'), rating=recipe_data.get('rating'), category=Category.objects.all()[0])[0]
    r.save()
    return r

if __name__ == '__main__':
    print("Populating database...")
    populate()
    print("Population complete")