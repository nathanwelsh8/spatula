from django.contrib import admin
from spatulaApp.models import Recipe, Category, UserProfile, RecipeImage, UserImage
# Register your models here.

admin.site.register(Recipe) 
admin.site.register(Category)
admin.site.register(UserImage)
admin.site.register(UserProfile)
admin.site.register(RecipeImage)
