"""spatula_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from spatulaApp import urls
#from spatulaApp import views as spatula_view
from django.urls import path 
from django.urls import include 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import handler404, handler500

from django.contrib.sitemaps.views import sitemap
from sitemaps import UserProfileSitemap, RecipeSitemap, StandardPageSitemap

sitemaps = {
    'userprofiles': UserProfileSitemap,
    'recipes': RecipeSitemap,
    'standard_pages': StandardPageSitemap,
}

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('spatulaApp.urls')), # try spatulaApp.urls if not work,
    path('search/',include("spatulaSearchAPI.urls")),
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}, name='sitemap'),
]

urlpatterns += staticfiles_urlpatterns()

handler404 = "spatulaApp.views.error_404"
handler500 = "spatulaApp.views.error_500"