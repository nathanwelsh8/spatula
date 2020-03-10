from django.contrib import admin
from spatulaApp.models import Recipe, UserProfile, Image, UserImage
# Register your models here.

admin.site.register(Recipe)
admin.site.register(UserProfile)
admin.site.register(Image)
admin.site.register(UserImage)