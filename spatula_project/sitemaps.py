from django.contrib.sitemaps import Sitemap
from spatulaApp.models import UserProfile, Recipe
from django.urls import reverse
 
 
class UserProfileSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.6
 
    def items(self):
        return UserProfile.objects.all()
 
 
class RecipeSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.8
 
    def items(self):
        return Recipe.objects.all()

class StandardPageSitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        # Return list of url names for views to include in sitemap
        return ['spatulaApp:index','spatulaApp:register']

    def location(self, item):
        return reverse(item)