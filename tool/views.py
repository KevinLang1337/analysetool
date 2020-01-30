from tool.DocumentReaderPDFMiner import process_pdf, get_data_wordcloud, get_data_foamtree
from django.shortcuts import render
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
from .models import Document
from .models import Configuration
import json

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
# https://blog.ekbana.com/pre-processing-text-in-python-ad13ea544dae nochmal anschauen
# https://datascience.blog.wzb.eu/2016/07/13/autocorrecting-misspelled-words-in-python-using-hunspell/

# Create your views here.
@csrf_exempt
def saveconfig(request):
    if request.method=="POST" and request.is_ajax():
        form = ConfigurationForm(request.POST)
        if form.is_valid():
    
            try:
                overwriteConfig = Configuration.objects.get(title=request.POST.get('title'))
                overwriteConfig.title = request.POST.get('title')
                overwriteConfig.topics = request.POST.get('topics')
                overwriteConfig.dateFrom = request.POST.get('dateFrom')
                overwriteConfig.dateUntil = request.POST.get('dateUntil')
                overwriteConfig.save()
                data = {'is_valid': True, 'title': overwriteConfig.title, 'id': overwriteConfig.id}
                
            except Configuration.DoesNotExist:
                overwriteConfig = None
                config = form.save()
                data = {'is_valid': True, 'title': config.title, 'id': config.id}
            return JsonResponse(data)
        else: return render(request, 'konfiguration.html')
    else: return render(request, 'konfiguration.html')


@csrf_exempt
def deleteconfig(request):
    if request.method=="POST" and request.is_ajax():
        config_id = int(request.POST.get('cid'))
        
        del_config = Configuration.objects.get(id=config_id)
        del_config.delete()
        return render(request, 'konfiguration.html')
    else: return render(request, 'konfiguration.html')

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

@csrf_exempt
def konfiguration(request):
    
    if request.method=="POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        
        if form.is_valid():

            document = form.save(commit=False)
            name, extension = os.path.splitext(document.file.name)
            document.extension = extension
            document.title = name
            document.save()

            print("Name: ", name, " | Typ: ", extension)

            data = {'is_valid': True, 'name': name, 'extension': extension, 'id': document.id}
            return JsonResponse(data)
        else:
            data = {'is_valid': False}

            return render(request, 'konfiguration.html', {'data':data})

    elif request.method=="GET": 
        document_list = Document.objects.all()
        config_list = Configuration.objects.all()
        return render(request, 'konfiguration.html', {'documents':document_list, 'configs': config_list})           


@csrf_exempt
def webcrawler(request):

    if request.is_ajax() and request.POST.get('action') == 'post':
        logging.debug("Hallo Keks!")
        amount = request.POST.get('amount')
        date_from = request.POST.get('date_from')
        date_until = request.POST.get('date_until')
        filenames = request.POST.getlist('filenames[]')
        print(*filenames)
        process_pdf(amount, date_from, date_until)
        

        return render(request, 'webcrawler.html')

    else:
        return render(request, 'webcrawler.html')


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
