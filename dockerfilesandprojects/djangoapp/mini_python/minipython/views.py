from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to cloud command classroom mini-python Django application!")

# Create your views here.
