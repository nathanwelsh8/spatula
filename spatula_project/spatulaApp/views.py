from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
# here so the database can be migrated without errors
def index(request):
    return HttpResponse("Hello World")