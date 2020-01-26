from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('konfiguration/', views.konfiguration, name='konfiguration'),
    path('webcrawler/', views.webcrawler, name='webcrawler'),
    path('ergebnisse/', views.ergebnisse, name='ergebnisse'),
    path('delete/', views.delete, name='delete'),
]
