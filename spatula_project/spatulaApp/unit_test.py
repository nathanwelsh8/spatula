import os

import re

import spatulaApp.models as app_model

from spatulaApp import forms

from databasePopulate import *

from datetime import datetime, timedelta

from django.db import models

from django.test import TestCase

from django.conf import settings

from django.urls import reverse, resolve

from django.contrib.auth.models import User

from django.forms import fields as django_fields

from django.contrib.auth import authenticate



#
#   README!  Please run python manage.py flush inbetween running tests
#   Otherwise a UNIQUE contraint fails due to storing multple instances of the same user object in the database!




FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}Spatula TEST FAILURE =({os.linesep}================{os.linesep}"

FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

class SettingsTests(TestCase):
    'Test the settings of django to ensure it is safe for deployment'

    def test_middleware_present(self):
        """

        Tests to see if the SessionMiddleware is present in the project configuration.

        """
        self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE)
    
    def test_session_app_present(self):
        """

        Tests to see if the SessionMiddleware is present in the project configuration.

        """

        self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE)
    def test_staticfiles_app_present(self):
        """ 
        Test that we have staticfile middleware present to allow for pythonanywhere deployment
        """
        self.assertTrue('django.contrib.staticfiles' in settings.INSTALLED_APPS)
    
    def test_media_urls_present(self):
        """
        Check media urls have been defined in settings
        """
        self.assertIsNot(settings.MEDIA_URL,None)
        self.assertNotEqual(settings.MEDIA_ROOT,None)
    
    def test_static_urls(self):
        """
        Check that the relevent static contants are defined for deployment
        """
        self.assertNotEqual(settings.STATIC_URL, None)
        self.assertNotEqual(settings.STATICFILES_DIRS,None)
    
    def test_static_loaders(self):
        """
        Check that essential static loaders are present during deployment 
        """
        self.assertTrue('django.contrib.staticfiles.finders.FileSystemFinder' in settings.STATICFILES_FINDERS)
        self.assertTrue('django.contrib.staticfiles.finders.AppDirectoriesFinder' in settings.STATICFILES_FINDERS)
    
    def test_ajax_core(self):
        """
        WebApp use AJAX and hence ensure that we have the relevent tools to 
        use AJAX defined in settings.
        """
        core = ['django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader']

        for c in core:
            self.assertTrue(c in settings.TEMPLATE_LOADERS)

class RecipeTest(TestCase):

    #setup params
    user = app_model.User.objects.get_or_create(username="test_user5",password="p3ssword")[0]
    print(type(user))
    user.set_password("p3ssword")
    user.save()

    user_profile = app_model.UserProfile.objects.get_or_create(user=user,bio="test text description")[0]
    user_profile.save()

    def fail_if_instanciate_by_user_profile_and_not_user_object(self):
        "check that postedby must be a User object and not a UserProfile object"
        self.assertRaises(Exception, app_model.Recipe(
            postedby=self.user_profile.id,
            name="test", method="test", 
            ingredients="test", 
            toolsreq="test", 
            difficulty=1,
            diettype=1, 
            cost=1, 
            category=app_model.Categories.get_or_create(name="test cat")[0].name).save()
            )

    def success_when_instanciate_by_user_id(self):
        "Check that the relationship between user and recipie holds"
        self.assertIsNotNone(app_model.Recipe(postedby=self.user.id,
        name="test", method="test", 
            ingredients="test", 
            toolsreq="test", 
            difficulty=1,
            diettype=1, 
            cost=1, 
            category=app_model.Categories.get_or_create(name="test cat")[0].name).save()
            )
    
    def slug_is_formed_correctly(self):
        "check that reipe slug is recipename and who posted the recipe"

        recipe = app_model.Recipe(postedby=self.user.id,
        name="test", method="test", 
            ingredients="test", 
            toolsreq="test", 
            difficulty=1,
            diettype=1, 
            cost=1, 
            category=app_model.Categories.get_or_create(name="test cat")[0].name
            )
        recipe.save()
        self.assertEqual(recipe.slug, str(recipe.name)+str(recipe.postedby))



class UserProfile(TestCase):

    user = app_model.User.objects.get_or_create(username="test_user4",password="p3ssword")[0]
    user.set_password("p3ssword")
    user.save()

    user_profile = app_model.UserProfile.objects.get_or_create(user=user,bio="test text description")[0]
    user_profile.save()

    def has_instrance_fields(self):
        "test that bio field is saved"
        self.assertIsNotNone(self.user_profile.bio)
        
    
    def user_profile_is_not_user(self):
        "check that UserProfile is not User"
        self.assertFalse(self.user == self.user_profile)
    
    def user_slug_is_name(self):
        " Checkk that the user slug is the username "
        self.assertEqual(user_profile.slug, user_profile.name)

    def users_can_authenticate(self):
        "check that created users can be authenticated"
        user = authenticate(username=user.username, password="p3ssword")
        self.assertIsNotNone(user)
