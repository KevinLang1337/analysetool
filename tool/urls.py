from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('konfiguration/', views.konfiguration, name='konfiguration'),
    path('webcrawler/', views.webcrawler, name='webcrawler'),
    path('ergebnisse/', views.ergebnisse, name='ergebnisse'),
    path('delete/', views.delete, name='delete'),
    path('saveconfig/', views.saveconfig, name='saveconfig'),
    path('crawlersaveconfig/', views.crawlersaveconfig, name='crawlersaveconfig'),
    path('deleteconfig/', views.deleteconfig, name='deleteconfig'),
    path('selectconfig/', views.selectconfig, name='selectconfig'),
    path('', include("django.contrib.auth.urls")),
    path('signup/', views.signup, name='signup'),
    path('saveurl/', views.saveurl, name='saveurl'),
    path('deletecrawlersource/', views.deletecrawlersource, name='deletecrawlersource'),
    
]
