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

import nltk, logging

def process_pdf():
    logging.debug("Analyse wird gestartet...")

    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

    dir = "tool/documents/"
    files_in_dir = [f for f in listdir(dir) if isfile(join(dir, f))]
    #print (files_in_dir)

    # obj = open('C:/Users/lanki/Documents/Uni/Semester 4/Masterarbeit/Test-Daten/Funktionsfähig/ipsum.txt', encoding="utf8")
    # for line in obj:
    #     print(line.rstrip())
    # obj.close()

    number_files = len(files_in_dir)
    dateTimeObj = datetime.now()

    print("Analyse von ", number_files, " Dokument/en wird gestartet...")

    # -----------------------------------
    # --- EXTRACT TEXT FROM DOCUMENTS ---
    # -----------------------------------

    extracted_text = ''
    for file in files_in_dir:
        #print("Analyse gestartet")
        fp = open(dir+file, 'rb')
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        parser.set_document(doc)
        # doc.set_parser(parser)
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
    # --- USE LEMMATIZATION ON EXTRACTED TEXT ----
    # --------------------------------------------

    import spacy
    nlp = spacy.load('de_core_news_sm')
    doc = nlp(extracted_text)
    extracted_text = " ".join([token.lemma_ for token in doc])

    word_tokens = word_tokenize(extracted_text) 

    # --------------------------------------------
    # --- DELETE NUMBERS FROM EXTRACTED TEXT -----
    # --------------------------------------------

    extracted_text = ''.join(c for c in extracted_text if not c.isdigit())

    # --------------------------------------------
    # --- DELETE STOPWORDS FROM EXTRACTED TEXT ---
    # --------------------------------------------

    stop_words = set(stopwords.words('german'))
    stopword_extension = ['(', ')', '.', ':', ',', ';', '!', '?', '´', '"', '“', '„', '»', '«',
                        '>', '<', '|', '–', '—', '_', '•', '...', '%', '!', '§', '!', '&', '/', '=', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\uf0b7', 'al', 'et', 'autor']
    stop_words.update(stopword_extension)  # -- erweitert die Stoppwortliste

                    

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    filtered_sentence = []


    # IF WORDS ARE NOT STOPWORD AND HAVE MORE CHARACTER THAN 3
    for w in word_tokens:
        if w not in stop_words and len(w) > 3:
            filtered_sentence.append(w)

    deleted_words = len(word_tokens) - len(filtered_sentence)
    print("Stopwords deleted: ", deleted_words)

    # # ----------------------------
    # # --- USE STEMMING ON TEXT ---
    # # ----------------------------

    # stemmer = SnowballStemmer('german')
    # stemmed_text = [stemmer.stem(word) for word in filtered_sentence]
    # stemmed_text.sort(key=len, reverse=True)
    # #print(stemmed_text)
    # counts = Counter(stemmed_text)

    counts = Counter(filtered_sentence)
    print('Most common:', counts.most_common(40))  # SHOWS 40 MOST COMMON TUPLE

    # print(counts)

    # -----------------------------------
    # --- LATENT DIRICHLET ALLOCATION ---
    # -----------------------------------

    # https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html
    # TODO: Stopwords, Stemming usw. für jedes Dokument einzeln machen. Dann die Liste mit Token einer anderen Liste hinzufügen
    # from gensim import corpora, models

    # dictionary = corpora.Dictionary(filtered_sentence)
    # corpus = [dictionary.doc2bow(text) for text in filtered_sentence]
    # print(corpus[0])
    



    # ----------------------------------
    # --- PRINT DURATION OF ANALYSIS ---
    # ----------------------------------

    dateTimeObjEnd = datetime.now()

    analyse_dauer = dateTimeObjEnd - dateTimeObj
    print("Analyse beendet")
    print("Analysedauer: ", analyse_dauer)

    # ---------------------
    # --- PLOTTING AREA ---
    # ---------------------

    # import matplotlib.pyplot as plt
    # import matplotlib as mpl
    # import numpy as np

    # x = np.linspace(0, 20, 100)
    # plt.plot(x, np.cos(x))
    # plt.show()

