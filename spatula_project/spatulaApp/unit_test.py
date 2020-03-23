import os

import re

import spatulaApp.models

from spatulaApp import forms

from databasePopulate import *

from datetime import datetime, timedelta

from django.db import models

from django.test import TestCase

from django.conf import settings

from django.urls import reverse, resolve

from django.contrib.auth.models import User

from django.forms import fields as django_fields


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
