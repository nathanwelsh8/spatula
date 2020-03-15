from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from spatulaApp.forms import UserForm, UserProfileForm, RecipeForm, RecipeImageUploadForm
from django.contrib.auth import authenticate, login, logout
from spatulaApp.models import Recipe, Category, RecipeImage, UserProfile
from django.urls import reverse 

# funky import that allows users to upload multiple images at once
from django.forms import modelformset_factory

# Create your views here.
# here so the database can be migrated without errors
def index(request):
    context_dict ={
        'recipies':Recipe.objects.order_by('rating'),
        'categories':Category.getModelsAsList,
        'diet_choices':Recipe.getChoicesAsList,
        'recipe_images': RecipeImage.objects.all(),
        }
        
    if request.method == 'POST': 
         username = request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(username=username, password=password)
         if user: 
              if user.is_active:
                   login(request, user)
                   return redirect(reverse('spatulaApp:index'))
              else: 
                   return HttpResponse("Your Rango account is disabled.")
         else:
              print(f"Invalid login details: {username}, {password}")
              return HttpResponse("Invalid login details supplied.")
    else:       
        for r in context_dict['recipies']: 
            r.rating = str(int(r.rating * 2))
        return render(request,'spatula/index.html', context_dict)
    
@login_required
def user_logout(request): 
    logout(request)
    # Take the user back to the homepage. 
    return redirect(reverse('spatulaApp:index'))

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
            return redirect(reverse('spatulaApp:index'))
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
    
    
@login_required
def add_recipe(request): 
    form = RecipeForm()
    context_dict = {}
    ImageFormSet = modelformset_factory(RecipeImage, form=RecipeImageUploadForm, extra=2, min_num=1, max_num=3) # extra =3 --> user can upload 3 images of recipe

    if request.method == 'POST': 
        form = RecipeForm(request.POST)   
        formset = ImageFormSet(request.POST, request.FILES,
        queryset = RecipeImage.objects.none()
        )     
        if form.is_valid() and formset.is_valid(): 
            recipe = form.save(commit=False)
            
            existingRecipe = Recipe.objects.filter(name=recipe.name)
            user = UserProfile.objects.get(user=request.user)

            # if the recipe exists, was it posed by our user?
            # if so do not allow them to resubmit the recipe
            if existingRecipe:
                canPost = True
                for r in existingRecipe:
                    if r.postedby == user:
                        canPost = False 
                        # will be displayed custom error message 
                        form._errors['name'] = form.error_class(['You have already poasted a recipe with this name.'])
                        break

            # only add if the recipe does not exist under our user
            if not existingRecipe or canPost:
                recipe.postedby = user
                recipe.save()

                for form in formset.cleaned_data:
                    if form:
                        image = form['image']
                        photo = RecipeImage(belongsto=Recipe.objects.get(name=recipe.name, postedby=user), image=image)
                        photo.save()

                return redirect(reverse('spatulaApp:index'))
        else: 
            print(form.errors, formset.errors)
    context_dict['form'] = form
    context_dict['formset'] = ImageFormSet(queryset=RecipeImage.objects.none())
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


