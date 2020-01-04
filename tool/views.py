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


nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
# https://blog.ekbana.com/pre-processing-text-in-python-ad13ea544dae nochmal anschauen
# https://datascience.blog.wzb.eu/2016/07/13/autocorrecting-misspelled-words-in-python-using-hunspell/

# Create your views here.

def konfiguration(request):
    return render(request, 'konfiguration.html')

def webcrawler(request):
    if 'crawlingButton' in request.GET:
        logging.debug("Hallo Keks!")
    return render(request, 'webcrawler.html')
  

def index(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

   
   
