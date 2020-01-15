from tool.DocumentReaderPDFMiner import process_pdf, get_data_wordcloud, get_data_temp
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

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from datetime import datetime


import nltk
import logging
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import DocumentUploadForm

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
# https://blog.ekbana.com/pre-processing-text-in-python-ad13ea544dae nochmal anschauen
# https://datascience.blog.wzb.eu/2016/07/13/autocorrecting-misspelled-words-in-python-using-hunspell/

# Create your views here.




@csrf_exempt
def konfiguration(request):
    if request.is_ajax() and request.method=='POST':
        logging.debug("Hallo Engel!")
        form=DocumentUploadForm(request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse(request, 'konfiguration.html')

    else: return render(request, 'konfiguration.html')


@csrf_exempt
def webcrawler(request):
    if request.is_ajax() and request.POST.get('action') == 'post':
        logging.debug("Hallo Keks!")
        amount = request.POST.get('amount')
        date_from = request.POST.get('date_from')
        date_until = request.POST.get('date_until')
        process_pdf(amount, date_from, date_until)
        return render(request, 'webcrawler.html')
    else:
        return render(request, 'webcrawler.html')


def index(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')


def ergebnisse(request):
    import json

    data_foamtree = {"groups": [
        {"id": "1", "label": "Thema 1", "groups": [
          {"id": "1.1", "label": "more", "groups": [
              {"id":"1.1.1", "label":"Beispieldokument.pdf"}, {"id":"1.1.1", "label":"InteressantesDokument2019.pdf"}

          ]},
          {"id": "1.2", "label": "text"}
        ]}]}

    test = get_data_temp()
    data = get_data_wordcloud()
    js_data= json.dumps(data)


    js_data2= json.dumps(data_foamtree)

    return render(request, 'results.html', {'dict_wordcloud': js_data, 'dict_foamtree': js_data2})
