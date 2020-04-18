from django.contrib.sitemaps import Sitemap
from spatulaApp.models import UserProfile, Recipe
 
 
class UserProfileSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.8
 
    def items(self):
        return UserProfile.objects.all()
 
 
class RecipeSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.9
 
    def items(self):
        return Recipe.objects.all()