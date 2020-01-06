# Test Push
from collections import Counter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

from os import listdir
from os.path import isfile, join

from datetime import datetime

import logging

def process_pdf():

    dir = "tool/documents/" # Directory to stored documents
    files_in_dir = [f for f in listdir(dir) if isfile(join(dir, f))] # all files in the directory
    
    number_files = len(files_in_dir) # amount of files in the directory
    
    dateTimeObj = datetime.now() # first timestamp for the duration of the analysis

    print("Analyse von ", number_files, " Dokument/en wird gestartet...")

    # --- EXTRACT TEXT FROM DOCUMENTS ---
    for file in files_in_dir:
        extracted_text = ''

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

        text_without_numbers = removeNumbers(extracted_text)
        text_without_stopwords = removeStopwords(text_without_numbers)
        lemmatizeTokens(text_without_stopwords)
        
# --- DELETE NUMBERS FROM EXTRACTED TEXT -----
def removeNumbers(text):
    temp_text = ''.join(c for c in text if not c.isdigit())
    return temp_text

# --- DELETE STOPWORDS FROM EXTRACTED TEXT ---   
def removeStopwords(text):
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

    stop_words = set(stopwords.words('german')) # model for german stopwords
    stopword_extension = ['(', ')', '.', ':', ',', ';', '!', '?', '´', '"', '“', '„', '»', '«',
                        '>', '<', '|', '–', '—', '_', '•', '...', '%', '!', '§', '!', '&', '/', '=', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\uf0b7', 'al', 'et', 'autor']
    stop_words.update(stopword_extension)  # expands the list of stopwords

    word_tokens = word_tokenize(text) 

    filtered_text = []

    # IF WORDS ARE NOT STOPWORD AND HAVE MORE CHARACTER THAN 3
    for w in word_tokens:
        if w not in stop_words and len(w) > 3:
            filtered_text.append(w)

    return filtered_text


# --- USE LEMMATIZATION ON EXTRACTED TEXT ----
def lemmatizeTokens(list_with_tokens):
    import spacy

    nlp = spacy.load('de_core_news_sm') # model for german texts
   
    list_to_str = ' '.join(token for token in list_with_tokens)

    doc = nlp(list_to_str)
    
    text = " ".join([token.lemma_ for token in doc])

    # for token in list_with_tokens:
    #     doc = nlp(token)
        
    #     print("Token: ", doc.token)
    #extracted_text = " ".join([token.lemma_ for token in doc])

    # counts = Counter(list_with_tokens)
    
    # return print('Most common:', counts.most_common(40))  # SHOWS 40 MOST COMMON TUPLE

#################################################################
# nlp = spacy.load('de_core_news_sm') # model for german texts
#     doc = nlp(extracted_text)
#     #extracted_text = " ".join([token.lemma_ for token in doc])

#     deleted_words = len(word_tokens) - len(filtered_text) # amount of deleted words
#     print("Stopwords deleted: ", deleted_words)

#     counts = Counter(filtered_text)
#     print('Most common:', counts.most_common(40))  # SHOWS 40 MOST COMMON TUPLE
#################################################################################


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

    # dateTimeObjEnd = datetime.now()

    # analyse_dauer = dateTimeObjEnd - dateTimeObj
    # print("Analyse beendet")
    # print("Analysedauer: ", analyse_dauer)


