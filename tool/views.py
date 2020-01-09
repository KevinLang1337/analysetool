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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
# https://blog.ekbana.com/pre-processing-text-in-python-ad13ea544dae nochmal anschauen
# https://datascience.blog.wzb.eu/2016/07/13/autocorrecting-misspelled-words-in-python-using-hunspell/

# Create your views here.

from tool.DocumentReaderPDFMiner import process_pdf

def konfiguration(request):
    if request.is_ajax():
        logging.debug("Hallo Engel!")
        
    else: return render(request, 'konfiguration.html')

@csrf_exempt
def webcrawler(request):
    if request.is_ajax() and request.POST.get('action') == 'post':
        logging.debug("Hallo Keks!")
        amount=request.POST.get('amount')
        date_from=request.POST.get('date_from')
        date_until=request.POST.get('date_until')
        process_pdf(amount, date_from, date_until)
        return render(request, 'webcrawler.html')
    else: 
        return render(request, 'webcrawler.html')
  

def index(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

   
   
