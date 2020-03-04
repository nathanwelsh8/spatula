from spatulaApp import views

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
 
 #add url patterns hereg
app_name = 'spatulaApp'
urlpatterns = [
     path('', views.index, name='index')
 ]
