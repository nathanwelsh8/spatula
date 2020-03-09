from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from spatulaApp.forms import UserForm, UserProfileForm, RecipeForm
from django.contrib.auth import authenticate, login, logout
from spatulaApp.models import Recipe, Category
from django.urls import reverse 

# Create your views here.
# here so the database can be migrated without errors
def index(request):
    context_dict ={
        'categories':Category.getModelsAsList,
        'diet_choices':Recipe.getChoicesAsList
        }
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

        if user_form.is_valid():
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
            return redirect(reverse('spatula:add_recipe'))
        else: 
            print(form.errors)
    context_dict['form'] = form
    return render(request, 'spatula/add_recipe.html', context=context_dict)


