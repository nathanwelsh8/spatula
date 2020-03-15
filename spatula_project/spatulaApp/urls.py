from spatulaApp import views

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
 
 #add url patterns hereg
app_name = 'spatulaApp'

# keep all urls lowercase
urlpatterns = [
     path('', views.index, name='index'),
     path('register/', views.register, name='register'),
     path('add_recipe/', views.add_recipe, name='add_recipe'),
     path('<slug:account_name_slug>/', views.show_profile, name='show_profile'),
     path('login/', views.user_login, name='login'),
     path('logout/', views.user_logout, name='logout'),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
