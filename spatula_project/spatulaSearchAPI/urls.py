from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from spatulaSearchAPI.views import search
app_name = 'spatulaSearchAPI'

# dont let users acess searchAPI
urlpatterns = [
     path('', search, name='search'),
 ] 
