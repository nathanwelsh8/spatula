import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'spatula_project.settings')

import django
from django.core.files import File

django.setup()

from spatulaApp.models import Category, Rating, UserProfile, Recipe, Image, RecipeImage, UserImage
from django.contrib.auth.models import User 
from spatula_project import settings
from datetime import datetime

def populate():
    users = [
        {'username': 'bob777', 'password': 'b3B123456', 'bio': 'Hi Im bob and i like cooking'},
        {'username': 'crazyman4', 'password': 'b3B123456', 'bio': 'I like cooking and getting crazy'},
        {'username': 'default_user', 'password': 'b3B123456', 'bio': 'None'},
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
    crazyman = UserProfile.objects.get(user=User.objects.get(username='crazyman4'))
    default_user = UserProfile.objects.get(user=User.objects.get(username='default_user'))
    recipies = {
        'Vegan Chilli':
        {
            'ingredients': '3 tbsp olive oil \n 2 sweet potatoes \n 1 onion \n 2 carrots \n 2 celery sticks \n 2 garlic cloves \n 2tsp chilli powder \n 2x400g chopped tomoatoes \n 400g can black beans \n 400g kidney beans',
            'toolsreq': 'Saucepan',
            'method': 'Heat oven to 200C/180C fan/gas 6. Put the sweet potato chunks in a roasting tin and drizzle over 1½ tbsp oil, 1 tsp smoked paprika and 1 tsp ground cumin. Give everything a good mix so that all the chunks are coated in spices, season with salt and pepper then roast for 25 mins until cooked. \n  Meanwhile, heat the remaining oil in a large saucepan over a medium heat. Add the onion, carrot and celery. Cook for 8-10 mins, stirring occasionally until soft then crush in the garlic and cook for 1 min more. Add the remaining dried spices and tomato puree. Give everything a good mix and cook for 1 min more.  \n Add the red pepper, chopped tomatoes and 200ml of water. Bring the chilli to a boil then simmer for 20 mins. Tip in the beans and cook for another 10 mins before adding the sweet potato. Season to taste then serve with lime wedges, guac, rice and coriander. Make ahead and freeze for up to 3 months. ',
            'difficulty': 2,
            'cost': 1,
            'diettype': 3,
            'rating': 3,
            'category': 'Mexican',
            'postedby': bob
        },
        'Chilli Con Carne':
            {
                'ingredients': '3 tbsp olive oil, 500g mince\n 1 onion\n 2 carrots\n 2 celery sticks\n 2 garlic cloves\n 2tsp chilli powder\n 2x400g chopped tomoatoes\n 400g can black beans\n 400g kidney beans',
                'toolsreq': 'Saucepan',
                'method': 'Heat a wok on a high heat and add the sunflower oil. Add the spring onions, garlic, ginger and stir-fry for 1 minute, then reduce the heat. Take care to not brown the vegetables. \n Add the carrot, red pepper and baby sweetcorn and stir-fry for 2 minutes. Add the mince, courgette and sugar snap peas and stir-fry for a further 3 minutes. Toss the ingredients from the centre to the side of the wok using a wooden spatula. Do not overcrowd the wok and keep the ingredients moving. \n Add 1 tablespoon water, hoisin and soy sauce and cook over a high heat for a further 2 minutes or until all the vegetables are cooked but not too soft. Serve with noodles or rice. \n',
                'difficulty': 1,
                'cost': 2,
                'diettype': 1,
                'rating': 3,
                'category': 'Mexican',
                'postedby': bob
            },
        'Cheese Toastie':
            {
                'ingredients':'Bread\n Cheese',
                'toolsreq': 'Grill',
                'method': 'Slice cheese and put between two slices of bread.\n Toast for 5 minutes in grill.',
                'difficulty': 1,
                'cost': 1,
                'diettype': 2,
                'rating': 3,
                'category': 'Western',
                'postedby': bob
            },
        'Scotch Broth':
            {
                'ingredients': '250g carrots\n 250g turnip\n 2 onions\n 1 celery stalk\n 1 leek\n 125g dried peas\n 4 pints lamb stock\n 85g kale\n 100g pearl barley',
                'toolsreq': 'Wok, Spatula',
                'method': 'Heat all of the ingredients, except the kale, in a large saucepan until boiling \n Reduce the heat and simmer gently for a 2-3 hours, or until the peas and pearl barley are soft. \n Stir in the kale and cook for a further 10-12 minutes, or until the kale is tender. Season, to taste, with salt and freshly ground black pepper.',
                'difficulty': 1,
                'cost': 1,
                'diettype': 3,
                'rating': 2,
                'category': 'Other',
                'postedby': bob
            },
        'Millionaire Shortbread':
            {
                'ingredients':'250g plain flour\n 75g caster sugar\n 300g butter\n 100g muscovado sugar\n 2x400g condensed milk\n 200g milk chocolate.',
                'toolsreq': 'Swiss Roll tin',
                'method': 'Heat the oven to 180C/160C fan/gas 4. Lightly grease a 33 x 23cm Swiss roll tin with a lip of at least 3cm. \n To make the shortbread, mix 250g plain flour and 75g caster sugar in a bowl. Rub in 175g softened butter until the mixture resembles fine breadcrumbs. \n Knead the mixture together until it forms a dough, then press into the base of the prepared tin. \n Prick the shortbread lightly with a fork and bake for 20 minutes or until firm to the touch and very lightly browned. Leave to cool in the tin. \n To make the caramel, place 100g butter or margarine, 100g light muscovado sugar and two 397g cans condensed milk in a pan and heat gently until the sugar has dissolved. \n To make the caramel, place 100g butter or margarine, 100g light muscovado sugar and two 397g cans condensed milk in a pan and heat gently until the sugar has dissolved. \n Bring to the boil, stirring all the time, then reduce the heat and simmer very gently, stirring continuously, for about 5-10 minutes or until the mixture has thickened slightly. Pour over the shortbread and leave to cool. \n For the topping, melt 200g plain or milk chocolate slowly in a bowl over a pan of hot water. Pour over the cold caramel and leave to set. Cut into squares or bars.  ',
                'difficulty': 2,
                'cost': 2,
                'diettype': 3,
                'rating': 3,
                'category': 'Other',
                'postedby': crazyman
            },
        'Vegetable Stir Fry':
            {
                'ingredients': '2 tbsp sunflower oil\n 4 spring onions\n 1 garlic clove\n piece fresh root ginger\n 1 carrot\n 1 red pepper\n 100g/3oz baby sweetcorn\n 1 courgette\n 150g/5oz sugar-snap peas\n 2 tbsp hoisin sauce\n 2 tbsp low-salt soy sauce',
                'toolsreq': 'Wok, Spatula',
                'method': 'Heat a wok on a high heat and add the sunflower oil. Add the spring onions, garlic, ginger and stir-fry for 1 minute, then reduce the heat. Take care to not brown the vegetables. \n Add the carrot, red pepper and baby sweetcorn and stir-fry for 2 minutes. Add the courgette and sugar snap peas and stir-fry for a further 3 minutes. Toss the ingredients from the centre to the side of the wok using a wooden spatula. Do not overcrowd the wok and keep the ingredients moving. \n Add 1 tablespoon water, hoisin and soy sauce and cook over a high heat for a further 2 minutes or until all the vegetables are cooked but not too soft. Serve with noodles or rice. \n',
                'difficulty': 1,
                'cost': 1,
                'diettype': 3,
                'rating': 3,
                'category': 'Chinese',
                'postedby': crazyman
            },
        'American Style Burger':
        {
            'ingredients': 'Mince\n Herbs\n Buns\n Eggs\n Seasioning\n Cheese',
            'toolsreq': 'Frying pan',
            'method': 'Fry burgers',
            'difficulty': 3,
            'cost': 2,
            'diettype': 1,
            'rating': 1,
            'category': 'Western',
            'postedby': crazyman
        }
    }

    print("Adding Recipes:")
    for recipe, recipe_data in recipies.items():
        r = add_recipe(recipe, recipe_data)
        print("\t Added", r)
    
    userImages = [
        {'image': 'userImage2.jpg' , 'belongsto': bob},
        {'image': 'userImage1.jpg', 'belongsto': crazyman},
        {'image':'profile.png','belongsto':default_user}
    ]
    print("Adding Profile Images:")
    for image in userImages:
           add_images(image)

    # you need to pass the object to the model not the string name.
    vsf = Recipe.objects.filter(name='Vegetable Stir Fry')[0]
    asb = Recipe.objects.filter(name='American Style Burger')[0]
    ratings = [
        {'recipe': vsf, 'rating': 5,'comment':'Really tasty, quick dinner. would recommend!'},
        {'recipe': vsf, 'rating': 3, 'comment':'Quick to make, even better when adding udon noodles!'},
        {'recipe': asb, 'rating': 4, 'comment':'Made this for a vegan and it made them cry. 10/10 would recommend'},
        {'recipe': asb, 'rating': 4, 'comment':'Best homemade burger ever!'},
        {'recipe': asb, 'rating': 5, 'comment':'Fantastic recipe, perfect for summer bbq!'},
        {'recipe': asb, 'rating': 3},
        {'recipe': asb, 'rating': 4},
        {'recipe': asb, 'rating': 4},
        {'recipe': asb, 'rating': 5},
        {'recipe': asb, 'rating': 3},
        {'recipe': asb, 'rating': 1, 'comment':'I followed the instructions and it burnt. not impressed!'},
        {'recipe': asb, 'rating': 4},
    ]
    print("Adding Ratings")
    for rating in ratings:
        add_rating(rating)
        
    vc = Recipe.objects.filter(name='Vegan Chilli')[0]
    ccc = Recipe.objects.filter(name='Chilli Con Carne')[0]    
    ct = Recipe.objects.filter(name='Cheese Toastie')[0]
    sb = Recipe.objects.filter(name='Scotch Broth')[0] 
    ms = Recipe.objects.filter(name='Millionaire Shortbread')[0] 
    
    recipeImages = [
        {'image': 'stir_fry_vegetables.jpg' , 'belongsto': vsf},
        {'image': 'burger.jpg', 'belongsto': asb}, 
        {'image': 'v_chilli.jpg' , 'belongsto': vc},
        {'image': 'chilli.jpg', 'belongsto': ccc},  
        {'image': 'cheese_toastie.jpg' , 'belongsto': ct},
        {'image': 'scotch_broth.jpg', 'belongsto': sb}, 
        {'image': 'millionaire_shortbread.jpg' , 'belongsto': ms},
    ]
    print("Adding Ratings")
    for image in recipeImages:
        add_recipe_images(image)    
    


def add_user(user_info):
    new_user = User.objects.get_or_create(username=user_info['username'], password=user_info['password'])[0]
    profile = UserProfile.objects.get_or_create(user=new_user, bio=user_info['bio'])[0]
    new_user.set_password(user_info['password'])
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
    
    r = Rating(recipe=recipe, rating=rating_info['rating'], comment=rating_info.get('comment',''))
    
    r.save()
    
def add_images(image): 
    i = UserImage(belongsto = image.get('belongsto'))
    i.image.save(image.get('image') + '.jpg', File(open(os.path.join(settings.STATIC_DIR, 'images/' + image.get('image')), 'rb')))
    print("\t Added", i)

def add_recipe_images(image): 
    i = RecipeImage(belongsto = image.get('belongsto'))
    i.image.save(image.get('image') + '.jpg', File(open(os.path.join(settings.STATIC_DIR, 'images/' + image.get('image')), 'rb')))
    print("\t Added", i)
    
if __name__ == '__main__':
    print("Populating database...")
    populate()
    print("Population complete")
    