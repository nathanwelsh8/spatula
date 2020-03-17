from spatulaApp import views

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

 #add url patterns hereg
app_name = 'spatulaApp'

# keep all urls lowercase
urlpatterns = [
     path('', views.index, name='index'),
     path('register/', views.register, name='register'),
     path('add_recipe/', views.add_recipe, name='add_recipe'),
     path('logout/', views.user_logout, name='logout'),

     #make sure this url is at the bottom so it doesn't match the other urls
     path('<slug:account_name_slug>/', views.show_profile, name='show_profile'),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
