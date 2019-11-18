from django.shortcuts import render

# Create your views here.

def konfiguration(request):
    return render(request, 'konfiguration.html')

def webcrawler(request):
    return render(request, 'webcrawler.html')

def index(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

from django.views import generic
   
   
