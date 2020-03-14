from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from spatulaApp.forms import UserForm, UserProfileForm, RecipeForm
from django.contrib.auth import authenticate, login, logout
from spatulaApp.models import Recipe, Category, UserProfile
from django.urls import reverse 

# Create your views here.
# here so the database can be migrated without errors
def index(request):
    context_dict ={
        'recipies':Recipe.objects.order_by('rating'),
        'categories':Category.getModelsAsList,
        'diet_choices':Recipe.getChoicesAsList,
        
        }
    for r in context_dict['recipies']: 
        r.rating = str(int(r.rating * 2))
    return render(request,'spatula/index.html', context_dict)


def register(request):
    # Using the same implementation as TWDjango

    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid()and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'spatula/register.html',
                  context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
    

def add_recipe(request): 
    form = RecipeForm()
    context_dict = {} 
    if request.method == 'POST': 
        form = RecipeForm(request.POST)
        
        if form.is_valid(): 
            form.save(commit=True)
            return redirect(reverse('spatula:index'))
        else: 
            print(form.errors)
    context_dict['form'] = form
    return render(request, 'spatula/add_recipe.html', context=context_dict)


def show_profile(request, account_name_slug):
    context_dict = {}

    try:
        # The .get() method returns one model instance or raises an exception.
        profile = UserProfile.objects.get(slug=account_name_slug)

        # Retrieve all of the associated recipes for this account.
        # recipes = Recipe.objects.filter(postedby=)

        # Add recipes to context dictionary
        # context_dict['recipes'] = recipes

        # Add profile object to context dictionary
        context_dict['profile'] = profile
    except UserProfile.DoesNotExist:
        return redirect(reverse('spatulaApp:index'))
    # Render response
    return render(request, 'spatula/profile.html', context=context_dict)


