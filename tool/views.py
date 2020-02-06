from tool.DocumentReaderPDFMiner import process_pdf, get_data_wordcloud, get_data_foamtree
from django.shortcuts import render, redirect
from django.views import generic
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

from os import listdir
from os.path import isfile, join
import os

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from datetime import datetime

import logging
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import DocumentUploadForm
from .forms import ConfigurationForm
from .forms import CrawlerConfigurationForm
from .forms import CrawlingurlsForm
from .models import Document
from .models import Configuration
from .models import Crawlingurls
from .models import CrawlerConfiguration
import json
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
# https://blog.ekbana.com/pre-processing-text-in-python-ad13ea544dae nochmal anschauen
# https://datascience.blog.wzb.eu/2016/07/13/autocorrecting-misspelled-words-in-python-using-hunspell/


# Creating a new user
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {"form":form})

# Saving a Configuration for analysis
@csrf_exempt
def saveconfig(request):
    if request.method=="POST" and request.is_ajax():
        form = ConfigurationForm(request.POST)
        if form.is_valid():
            doc_id = request.POST.getlist('documents[]')
            # Overwriting Configuration, if the user already has a Configuration with that title
            try:
                overwriteConfig = Configuration.objects.get(userID = request.user.id,title=request.POST.get('title'))
                overwriteConfig.title = request.POST.get('title')
                overwriteConfig.topics = request.POST.get('topics')
                overwriteConfig.dateFrom = request.POST.get('dateFrom')
                overwriteConfig.dateUntil = request.POST.get('dateUntil')
                overwriteConfig.userID = request.user.id
                overwriteConfig.save()
                overwriteConfig.documents.remove(*overwriteConfig.documents.all())
                for i in range(len(doc_id)):
                    save_doc = int(doc_id[i])
                    overwriteConfig.documents.add(Document.objects.get(id=save_doc))
                data = {'is_valid': True, 'title': overwriteConfig.title, 'id': overwriteConfig.id}
            # Saving a new Configuration if there is nothing to overwrite
            except Configuration.DoesNotExist:
                overwriteConfig = None
                config = form.save()
                config.userID = request.user.id
                config.save()
                for i in range(len(doc_id)):
                    save_doc = int(doc_id[i])
                    config.documents.add(Document.objects.get(id=save_doc))
                
                data = {'is_valid': True, 'title': config.title, 'id': config.id}
            return JsonResponse(data)
        else: return render(request, 'konfiguration.html')
    else: return render(request, 'konfiguration.html')

# Deleting a Configuration for an analysis
@csrf_exempt
def deleteconfig(request):
    if request.method=="POST" and request.is_ajax():
        config_id = int(request.POST.get('cid'))
        
        del_config = Configuration.objects.get(id=config_id)
        del_config.delete()
        return render(request, 'konfiguration.html')
    else: return render(request, 'konfiguration.html')

# Sending values of selected Configuration to the template
def selectconfig(request):
    if request.method=="GET" and request.is_ajax():
        config_id = int(request.GET.get('configID'))
        select_config = Configuration.objects.get(id=config_id)
        id_list = []
        for document in select_config.documents.all():
            id_list.append(document.id)
        data = {'is_valid': True, 'id_list': id_list,'topics': select_config.topics, 'dateFrom': select_config.dateFrom, 'dateUntil': select_config.dateUntil}
        return JsonResponse(data)
    else: return render(request, 'konfiguration.html')

# Deleting a Document
@csrf_exempt
def delete(request):
    if request.method=="POST" and request.is_ajax():
        doc_id = request.POST.getlist('doc_id[]')
        for i in range(len(doc_id)):
            delete_doc = int(doc_id[i])
            document = Document.objects.get(id=delete_doc)
            document.delete()
        return render(request, 'konfiguration.html')
    else: return render(request, 'konfiguration.html')

# Deleting an URL
@csrf_exempt
def deletecrawlersource(request):
    if request.method=="POST" and request.is_ajax():
        url_id = request.POST.getlist('url_id[]')
        for i in range(len(url_id)):
            delete_url = int(url_id[i])
            url = Crawlingurls.objects.get(id=delete_url)
            url.delete()
        return HttpResponse()
    else: return render(request, 'webcrawler.html')


@csrf_exempt
def konfiguration(request):
    
    if request.method=="POST":
        # Uploading a Document and sending its properties back to template
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():

            document = form.save(commit=False)
            name, extension = os.path.splitext(document.file.name)
            document.extension = extension
            document.title = name
            document.userID = request.user.id
            document.save()

            print("Name: ", name, " | Typ: ", extension)

            data = {'is_valid': True, 'name': name, 'extension': extension, 'id': document.id}
            return JsonResponse(data)
        else:
            data = {'is_valid': False}

            return render(request, 'konfiguration.html', {'data':data})
    # Populate template with user specific Documents and Configurations
    elif request.method=="GET": 
        document_list = Document.objects.filter(userID=request.user.id)
        config_list = Configuration.objects.filter(userID=request.user.id)
        return render(request, 'konfiguration.html', {'documents':document_list, 'configs': config_list})           

# Saving a URL for crawling
@csrf_exempt
def saveurl(request):
    if request.method=="POST" and request.is_ajax():
        form = CrawlingurlsForm(request.POST)
        if form.is_valid():
            new_url = form.save(commit =False)
            hallo = request.POST.get('title')
            print(hallo)
            new_url.title = request.POST.get('title')
            new_url.userID = request.user.id
            new_url.save()
            data = {'is_valid': True, 'title':new_url.title, 'id': new_url.id}
            return JsonResponse(data)
        else: 
            data = {'is_valid': False}
            return JsonResponse(data)
    else: return render(request, 'webcrawler.html')

# Saving a Configuration for crawling
@csrf_exempt
def crawlersaveconfig(request):
    if request.method=="POST" and request.is_ajax():
        form = CrawlerConfigurationForm(request.POST)
        if form.is_valid():
            doc_id = request.POST.getlist('documents[]')
            # Overwriting Configuration, if the user already has a Configuration with that title
            try:
                overwriteConfig = Configuration.objects.get(userID = request.user.id,title=request.POST.get('title'))
                overwriteConfig.title = request.POST.get('title')
                overwriteConfig.topics = request.POST.get('topics')
                overwriteConfig.dateFrom = request.POST.get('dateFrom')
                overwriteConfig.dateUntil = request.POST.get('dateUntil')
                overwriteConfig.userID = request.user.id
                overwriteConfig.save()
                overwriteConfig.documents.remove(*overwriteConfig.documents.all())
                for i in range(len(doc_id)):
                    save_doc = int(doc_id[i])
                    overwriteConfig.documents.add(Document.objects.get(id=save_doc))
                data = {'is_valid': True, 'title': overwriteConfig.title, 'id': overwriteConfig.id}
            # Saving a new Configuration if there is nothing to overwrite
            except Configuration.DoesNotExist:
                overwriteConfig = None
                config = form.save()
                config.userID = request.user.id
                config.save()
                for i in range(len(doc_id)):
                    save_doc = int(doc_id[i])
                    config.documents.add(Document.objects.get(id=save_doc))
                
                data = {'is_valid': True, 'title': config.title, 'id': config.id}
            return JsonResponse(data)
        else: return render(request, 'webcrawler.html')
    else: return render(request, 'webcrawler.html')

@csrf_exempt
def webcrawler(request):

    if request.is_ajax() and request.POST.get('action') == 'post':
        logging.debug("Hallo Keks!")
        amount = request.POST.get('amount')
        date_from = request.POST.get('date_from')
        date_until = request.POST.get('date_until')
        file_ids = request.POST.getlist('file_ids[]')
        
        process_pdf(amount, date_from, date_until, file_ids)
        

        return render(request, 'webcrawler.html')

    elif request.method=="GET": 
        urls_list = Crawlingurls.objects.filter(userID=request.user.id)
        crawler_config_list = CrawlerConfiguration.objects.filter(userID=request.user.id)
        return render(request, 'webcrawler.html', {'urls':urls_list, 'crawler_configs': crawler_config_list})   


def index(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')


def ergebnisse(request):
    import json
    
    # temp_dict = {"label": "Thema 1"}
    # temp_dict2 = {"label": "Thema 2"}
    # temp_dict3 = {"label": "Thema 3"}
    # temp_list = []
    # temp_list.append(temp_dict)
    # temp_list.append(temp_dict2)
    # temp_list.append(temp_dict3)

    data_foamtree = get_data_foamtree() #{"groups": temp_list}
    
    # {"groups": [
    #     {"label": "Thema 1", "groups": [
    #       {label": "more", "groups": [
    #           {"label":"Beispieldokument.pdf"}, {"label":"InteressantesDokument2019.pdf"}

    #       ]},
    #       {"id": "1.2", "label": "text"}
    #     ]}]}

    
    data = get_data_wordcloud()
    js_data= json.dumps(data)
    js_data2= json.dumps(data_foamtree)

    return render(request, 'results.html', {'dict_wordcloud': js_data, 'dict_foamtree': js_data2})
