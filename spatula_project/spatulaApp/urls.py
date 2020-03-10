from spatulaApp import views

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
 
 #add url patterns hereg
app_name = 'spatulaApp'
urlpatterns = [
     path('', views.index, name='index'),
     path('register', views.register, name='register'),
     path('add_recipe/', views.add_recipe, name='add_recipe'),
     # will change profile path to  '<slug:account_name_slug>/'
     path('profile', views.profile, name='profile'),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
