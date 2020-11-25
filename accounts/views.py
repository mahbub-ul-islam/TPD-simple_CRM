from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def home(request):
    return HttpResponse('Home Page')

def products(request):
    return HttpResponse('Products page')

def customer(request):
    return HttpResponse('Customer Page')
