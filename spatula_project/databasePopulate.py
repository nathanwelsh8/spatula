import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'spatula_project.settings')

import django
django.setup()

from spatulaApp.models import Category


def populate():    

    categories = [
        {
            'name':'Italian',

        },
        {
            'name':'Chinese'
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
            'name':'Mexican'
        },
        {
            'name':'Other'
        }
    ]

    for cat in categories:
        c = add_category(cat)
        print("\t Added",c)
    


def add_category(category_dict):
    c = Category.objects.get_or_create(name=category_dict['name'])[0]
    c.save()
    return c

if __name__ == '__main__':
    print("Populating database...")
    populate()
    print("Population complete")