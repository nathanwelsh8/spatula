import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'spatula_project.settings')

import django
django.setup()

from ramgo.models import Category

def populate():

    categories = [
        {
            'name':'Italian',

        },
        {
            'name':'Chineese'
        },
        {
            'name':'Thai'
        },
        {
            'name':'Western'
        },
        {
            'name':'Indian'
        },
        {
            'name':'mexican'
        },
        {
            'name':'Other'
        }
    ]

def add_category(category_dict):
    pass