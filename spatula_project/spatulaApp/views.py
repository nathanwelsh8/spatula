from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from spatulaApp.forms import UserForm, UserProfileForm, UserProfileUpdateForm, RecipeForm, RecipeImageUploadForm,CommentForm,ProfileImageUploadForm
from django.contrib.auth import authenticate, login, logout

from spatulaSearchAPI.forms import SearchForm
from spatulaApp.models import Recipe, Category, RecipeImage, UserProfile, Rating, UserImage
from django.urls import reverse 
from spatulaSearchAPI.views import search as API_Search
from spatulaSearchAPI.views import non_http_search as non_http_API_search
from django.views import View

# funky import that allows users to upload multiple images at once
from django.forms import modelformset_factory

# Create your views here.
# here so the database can be migrated without errors

# instead of displaying 404, keep things simple by redirecting to index
def error_404(request, *args, **kwargs):
    return redirect(reverse('spatulaApp:index'))

# This needs its own page as it an internal
# server error, loading a page which is dynamic
# is not possible so display static html
def error_500(request, *args,**kwargs):
    return HttpResponse("spatula/500.html")
    # return redirect(reverse('spatulaApp:index'))

class Index(View):

    recipe_cache = None

    def search(self, request, cache=None):
        return API_Search(request, cache=cache)
    def fix_ratings(self):

        # map ratings to integer values and sanitise edge cases
        for r in self.context_dict['recipies']: 
            r.rating = str(round(int(r.rating * 2)))
            if int(r.rating) >5:
                r.rating= str(5)
            elif int(r.rating) <0:
                r.rating = str(0)
                

    # Data to be passed into page
    context_dict ={

        'recipies':"",# ajax will get the recipies when document is ready.
        'categories':Category.getModelsAsList,
        'diet_choices':Recipe.getChoicesAsList,
        'recipe_images': RecipeImage.objects.all(),
        'user_pic':None,
        'login_error_msg':None,
        'runPreSearch':True
        }

    def get(self, request, **kwargs):
        if kwargs.get('login_error_msg'):
            self.context_dict['login_error_msg'] =  kwargs['login_error_msg']
        else:
            self.context_dict['login_error_msg'] = None

        if 'search' in request.GET:
            # get users live search criteria
            if not self.recipe_cache:
                self.recipe_cache = Recipe.objects.all()

            self.context_dict['recipies'] = self.search(request, cache=self.recipe_cache)

            self.fix_ratings()
            return render(request, 'spatulaSearchAPI/results.html',self.context_dict)
        
        elif 'redirect_search_text' in request.GET:
            self.context_dict['runPreSearch'] = False
            
            json_req = {}
            json_req['search'] = request.GET['redirect_search_text']
            
            self.context_dict['recipies'] = non_http_API_search(json_req)
        else:
            self.context_dict['runPreSearch'] = True

        self.fix_ratings() # multiply by 2 so they are mapped to a stars rating
        self.context_dict['recipe_images'] = RecipeImage.objects.all()  
        self.context_dict['user_pic'] = UserImage.objects.filter(belongsto=request.user.id) 
        print(request.user.id)
        return render(request, 'spatula/index.html', self.context_dict)

    def post(self, request):
         
        username = request.POST.get('username')
        password = request.POST.get('password')

        # If they clicked the register button they are redirected to register page.
        if 'register' in request.POST:
            return redirect(reverse('spatulaApp:register'))

        user = authenticate(username=str(username.lower()), password=str(password))
        
        if user: 
            if user.is_active:
                login(request, user)
                return redirect(reverse('spatulaApp:index'))
            else: 
                return self.get(request, **{"login_error_msg":"Your Spatula account has been disabled."})
                
        else:
            return self.get(request, **{"login_error_msg":"Invalid login details supplied."})
    
    
@login_required(login_url='spatulaApp:index')
def user_logout(request): 
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('spatulaApp:index'))
    

class Register(View):

    def post(self,request):

        registered = False
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid()and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            user.username = user.username.lower()
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
            profile.bio = profile_form['bio'].data
            profile.save()
            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
            
            user = authenticate(username=user.username.lower(), password=user_form['password'].data)
            if user:
                login(request, user)
                
            return redirect(reverse('spatulaApp:index'))
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors)

            return self.get(request,context={'registered':registered})
    
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
    

    def get(self,request, context=None):

        if not context:
            context = {}
        user_form = UserForm()
        profile_form = UserProfileForm()
        
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        
        return render(request, 'spatula/register.html',
                  context=context)  

  
@login_required(login_url="spatulaApp:index")
def add_recipe(request): 
    form = RecipeForm()
    context_dict = {
            'user_pic': UserImage.objects.all(),
    }
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
                        form._errors['name'] = form.error_class(['You have already posted a recipe with this name.'])
                        break

            # only add if the recipe does not exist under our user
            if not existingRecipe or canPost:
                recipe.postedby = user
                recipe.save()

                success = False
                for form in formset.cleaned_data:
                    print("form:",form)
                    if form:
                        image = form['image']
                        if image:
                            print("Image:",image)
                            photo = RecipeImage(belongsto=Recipe.objects.get(name=recipe.name, postedby=user), image=image)
                            photo.save()
                            success = True
                if success:
                    recipe.save() # only save image if we have a recipe image
                    return redirect(reverse('spatulaApp:index'))
                else:
                    context_dict['form'] = form
                    context_dict['formset'] = ImageFormSet(queryset=RecipeImage.objects.none())
                    return render(request, 'spatula/add_recipe.html', context=context_dict)

        else: 
            print(form.errors, formset.errors)
    context_dict['form'] = form
    context_dict['formset'] = ImageFormSet(queryset=RecipeImage.objects.none())
    return render(request, 'spatula/add_recipe.html', context=context_dict)


class ShowProfile(View):

    def fix_ratings(self):
    
        # map ratings to integer values and sanitise edge cases
        for r in self.context_dict['recipies']: 
            r.rating = str(round(int(r.rating * 2)))
            if int(r.rating) >5:
                r.rating= str(5)
            elif int(r.rating) <0:
                r.rating = str(0)

    context_dict = {
            'user_pic': UserImage.objects.all(),
    }
    user_cache = None

    def get(self, request,account_name_slug=None):

        # If a user enters a bogus url which gets mapped to this view then 
        # we want to redirect to the homepage and not search the db for the
        # 'slug url'. 
        try:
            if self.user_cache is None:
                self.user_cache = UserProfile.objects.get(user=User.objects.get(username=account_name_slug).id)

            # The .get() method returns one model instance or raises an exception.
            profile = UserProfile.objects.get(slug=account_name_slug)
            # Retrieve all of the associated recipes for this account.
            recipes = Recipe.objects.filter(postedby=self.user_cache.id)
            # Add recipes to context dictionary
            self.context_dict['recipies'] = recipes

            # Add profile object to context dictionary
            self.context_dict['profile'] = profile


            # if there is a logged in user who 'owns' the profile page
            # let them edit it. if there is a logged in user who is admin
            # let them make edits too ;)
            self.context_dict['canEdit'] =  (request.user == profile.user) or request.user.is_superuser 
            
            # if user is allowed to edit, allow them to upload an profile pic
            self.context_dict['image_form'] = None
            if self.context_dict['canEdit']:
                self.context_dict['image_form'] = ProfileImageUploadForm()
            
            self.context_dict['profile_pic'] = UserImage.objects.get(belongsto=self.user_cache.id) # try to retrieve users profile pic

        except User.DoesNotExist:
            return redirect(reverse('spatulaApp:index'))
        except UserProfile.DoesNotExist:
            return redirect(reverse('spatulaApp:index'))
        except UserImage.DoesNotExist:
            self.context_dict['profile_pic'] = None # users has no profile pic so use default


        # get the recipes belonging to this user
        if request.GET.get('get_recipes',None) == "getUser":
            self.context_dict['recipe_images'] = []
            for recipe in self.context_dict['recipies']:
                self.context_dict['recipe_images'].append(RecipeImage.objects.filter(belongsto=recipe.id))
            
            #recipies already present in context dict so just tell the template to update
            return render(request,'spatulaSearchAPI/results.html',self.context_dict)

        # if user tries to search through the recipies associated with this user
        # uses the same search API used for index page
        elif 'search' in request.GET:
            self.context_dict['recipies'] = API_Search(request,user_filter=self.user_cache.id)
            self.fix_ratings()
            return render(request, 'spatulaSearchAPI/results.html',self.context_dict)

        self.context_dict['user_pic'] = UserImage.objects.all()

        return render(request, 'spatula/profile.html', context=self.context_dict)


    def post(self,request, account_name_slug=None):
        try:
            if self.user_cache is None:
                self.user_cache = UserProfile.objects.get(user=User.objects.get(username=account_name_slug).id)
            # The .get() method returns one model instance or raises an exception.
            
            profile = self.user_cache #UserProfile.objects.get(slug=account_name_slug)
            
            # Retrieve all of the associated recipes for this account.
            recipes = Recipe.objects.filter(postedby=self.user_cache.id)
            # Add recipes to context dictionary
            
            self.context_dict['recipies'] = recipes

            # Add profile object to context dictionary
            self.context_dict['profile'] = profile
            
        except UserProfile.DoesNotExist:
            return redirect(reverse('spatulaApp:index'))
        except User.DoesNotExist:
            return redirect(reverse('spatulaApp:index'))
        
        if request.POST.get('update_bio',None): # if user updates bio
            self.user_cache.bio = request.POST['update_bio']
            self.user_cache.save()
            return render(request, 'spatula/profile.html', context=self.context_dict)
        
        elif request.POST.get('update_profile_pic',None): # if user updates profile image
            form = ProfileImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                #form.belongsto = self.user_cache.id
                image = form['image'].data
                if image:
                    photo = UserImage(belongsto=self.user_cache, image=image)
                    UserImage.objects.filter(belongsto=self.user_cache).delete() #only allowed 1 profile pic
                    photo.save()
                    self.context_dict['profile_pic'] = photo 

        elif request.POST.get('delete_profile',None):
            print("delete_profile")
            if self.context_dict['canEdit']: # stops javascript console injection
                try:
                    print("Deleting", self.user_cache)
                    #Get all recipes to delete
                    del_recipes = Recipe.objects.filter(postedby=self.user_cache.id)
                    
                    # delete all images linked to these recipes
                    for recipe in del_recipes:
                        print(recipe)
                        images = RecipeImage.objects.filter(belongsto=recipe.id).delete()
                        print("\tdeleted images")
                        #delete the recipe
                        recipe.delete()
                        print("\tdeleted recipe")
                    #   Delete users profile pic
                    #   Use filter as it may be none

                    UserImage.objects.filter(belongsto=self.user_cache.id).delete()
                    print("\tdeleted profile pic")
                    # Finally delete the user from db
                    UserProfile.objects.get(id=self.user_cache.id).delete()
                    print("\deleted UserProfile")
                    User.objects.get(username=request.user).delete()
                    print("DeletedUser")
                except UserProfile.DoesNotExist:
                    print("Profile not exist")
                except User.DoesNotExist:
                    print("User object not exist")
                finally:
                    print("redirecting..")
                    return redirect(reverse('spatulaApp:index'))

        return render(request, 'spatula/profile.html', context=self.context_dict)


class RecipePage(View):

    context_dict = {
            'user_pic': UserImage.objects.all(),
    }
    form = CommentForm()
    recipe_cache = None
    user_cache = None

    def fix_ratings(self):

        # use a class based context dict to allow caching queries
        # when getting / posting secondry requests
        self.context_dict['recipe'].rating = str(round(int(self.context_dict['recipe'].rating * 2)))
        if int(self.context_dict['recipe'].rating) >5:
            self.context_dict['recipe'].rating= str(5)
        elif int(self.context_dict['recipe'].rating) <0:
            self.context_dict['recipe'].rating = str(0)
    
    def post(self,request, recipe_slug_name):
        
        # deal with POST requests that want to
        # edit an existing recipe
        if request.POST.get('update_recipe', False):
            recipe = Recipe.objects.get(slug=recipe_slug_name)
            recipe.difficulty = request.POST['difficulty']
            recipe.cost = request.POST['cost']
            recipe.method = request.POST['method']
            recipe.ingredients = request.POST['ingredients']
            recipe.toolsreq = request.POST['tools']
            recipe.category = Category.objects.get(name=request.POST['category'])
            # recipe.diettype = request.POST['diet']
            recipe.save()
            return redirect(reverse('spatulaApp:index'))


        form = CommentForm(request.POST)
        if self.recipe_cache is None:
                    self.recipe_cache = Recipe.objects.get(slug = recipe_slug_name)

        if form.is_valid(): 

            comment = form.save(commit=False)
            existingComments = Rating.objects.filter(recipe=self.recipe_cache.id )
            
            try:
                if self.user_cache is None:
                    self.user_cache = UserProfile.objects.get(user=User.objects.get(username=request.user))
            except UserProfile.DoesNotExist:
                print("Admin has not linked their user profile!")
                return render(request, 'spatula/recipe.html')

            # existing reviews, was one posted by our user?
            # if so do not allow them to submit another review
            if existingComments:
                canPost = True
                for r in existingComments:
                    if r.postedby.__str__()== request.user.username:
                        canPost = False 
                        # will be displayed custom error message 
                        form._errors['comment'] = form.error_class(['You have already left a review on this recipe!'])
                        break
            
            # only add if the recipe does not exist under our user
            # and if the submitted user does not own the recipe
            if not existingComments or canPost:
                if not self.user_cache == self.recipe_cache.postedby:
                    comment.postedby = self.user_cache
                    
                    comment.recipe = self.recipe_cache
                    comment.save()
                    return redirect(reverse('spatulaApp:index'))
                else:
                    form._errors['comment'] = form.error_class(['You cannot post your own comment!'])
            
                 


        self.context_dict['recipe'] = self.recipe_cache
        self.fix_ratings()
        #form._errors['name'] = form.error_class(['You need to leave a rating!'])
        self.context_dict['form'] = form
        return render(request, 'spatula/recipe.html', context = self.context_dict)
                    
    def get(self,request,recipe_slug_name):
        #todo add cache
        try:
            if self.recipe_cache is None:
                self.recipe_cache = Recipe.objects.get(slug = recipe_slug_name)
           
        except Recipe.DoesNotExist:
            return redirect(reverse('spatulaApp:index'))
        

        if 'search' in request.GET:
            print("search request recieved")
            #self.context_dict['recipies'] = API_Search(request,user_filter=self.user_cache.id)
            #self.fix_ratings()
            return redirect(reverse( 'spatulaApp:index'))


        self.context_dict['recipe'] = self.recipe_cache
        self.context_dict['user_images'] = UserImage.objects.all();
        # There may ve alot of comments and images so reduce load by 
        # only passing in images and comments relevent to this recipe
        self.context_dict['images'] = RecipeImage.objects.filter(belongsto=self.recipe_cache.id)
        self.context_dict['reviews'] = Rating.objects.filter(recipe=self.recipe_cache.id)
        self.context_dict['form'] = self.form

        # if there is a logged in user who 'owns' the recipe
        # let them edit it. if there is a logged in user who is admin
        # let them make edits too ;)
        recipe = Recipe.objects.get(slug=recipe_slug_name)
        profile = recipe.postedby
        self.context_dict['canEdit'] = (request.user == profile.user) or request.user.is_superuser
        self.context_dict['categories'] = Category.getModelsAsList()
        diet_choices = [choice[1] for choice in Recipe.DIET_CHOICES]
        self.context_dict['diet_choices'] = diet_choices

        self.fix_ratings()
        return render(request, 'spatula/recipe.html', context = self.context_dict)

