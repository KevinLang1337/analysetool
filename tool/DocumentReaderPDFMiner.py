# Test Push
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

import nltk, logging, spacy

def process_pdf():
   
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

    dir = "tool/documents/" # Directory to stored documents
    files_in_dir = [f for f in listdir(dir) if isfile(join(dir, f))] # all files in the directory
    #print (files_in_dir)
    number_files = len(files_in_dir) # amount of files in the directory
    dateTimeObj = datetime.now() # first timestamp for the duration of the analysis

    print("Analyse von ", number_files, " Dokument/en wird gestartet...")


    # -----------------------------------
    # --- EXTRACT TEXT FROM DOCUMENTS ---
    # -----------------------------------

    extracted_text = ''
    #LOOPS EVERY PDF IN THE DIRECTORY AND STORES THE TEXT TO extracted_text
    for file in files_in_dir:
        fp = open(dir+file, 'rb')
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        parser.set_document(doc)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        laparams.char_margin = 1.0
        laparams.word_margin = 1.0
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    extracted_text += lt_obj.get_text()


    # --------------------------------------------
    # --- DELETE NUMBERS FROM EXTRACTED TEXT -----
    # --------------------------------------------

    extracted_text = ''.join(c for c in extracted_text if not c.isdigit())

    # --------------------------------------------
    # --- DELETE STOPWORDS FROM EXTRACTED TEXT ---
    # --------------------------------------------

    stop_words = set(stopwords.words('german')) # model for german stopwords
    stopword_extension = ['(', ')', '.', ':', ',', ';', '!', '?', '´', '"', '“', '„', '»', '«',
                        '>', '<', '|', '–', '—', '_', '•', '...', '%', '!', '§', '!', '&', '/', '=', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\uf0b7', 'al', 'et', 'autor']
    stop_words.update(stopword_extension)  # expands the list of stopwords

    word_tokens = word_tokenize(extracted_text) 

    filtered_text = []

    # IF WORDS ARE NOT STOPWORD AND HAVE MORE CHARACTER THAN 3
    for w in word_tokens:
        if w not in stop_words and len(w) > 3:
            filtered_text.append(w)

    # --------------------------------------------
    # --- USE LEMMATIZATION ON EXTRACTED TEXT ----
    # --------------------------------------------

    nlp = spacy.load('de_core_news_sm') # model for german texts
    doc = nlp(extracted_text)
    #extracted_text = " ".join([token.lemma_ for token in doc])

    deleted_words = len(word_tokens) - len(filtered_text) # amount of deleted words
    print("Stopwords deleted: ", deleted_words)

    counts = Counter(filtered_text)
    print('Most common:', counts.most_common(40))  # SHOWS 40 MOST COMMON TUPLE


    # -----------------------------------
    # --- LATENT DIRICHLET ALLOCATION ---
    # -----------------------------------

    # https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html
    # TODO: Stopwords, Stemming usw. für jedes Dokument einzeln machen. Dann die Liste mit Token einer anderen Liste hinzufügen
    # from gensim import corpora, models

    # dictionary = corpora.Dictionary(filtered_text)
    # corpus = [dictionary.doc2bow(text) for text in filtered_text]
    # print(corpus[0])


    # ----------------------------------
    # --- PRINT DURATION OF ANALYSIS ---
    # ----------------------------------

    dateTimeObjEnd = datetime.now()

    analyse_dauer = dateTimeObjEnd - dateTimeObj
    print("Analyse beendet")
    print("Analysedauer: ", analyse_dauer)


