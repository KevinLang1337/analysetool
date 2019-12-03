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
#nltk.download('stopwords') //MUSS INITIAL EINMAL AUSGEFÜHRT WERDEN
#nltk.download('punkt') //MUSS INITIAL EINMAL AUSGEFÜHRT WERDEN
#set(stopwords.words('german'))
#set(stopwords.words('english'))

dir = 'C:/Users/lanki/Documents/Uni/Semester 4/Masterarbeit/Test-Daten/funktionsfähig/'
files_in_dir = [f for f in listdir(dir) if isfile(join(dir, f))]
#print (files_in_dir)

# obj = open('C:/Users/lanki/Documents/Uni/Semester 4/Masterarbeit/Test-Daten/Funktionsfähig/ipsum.txt', encoding="utf8")
# for line in obj:
#     print(line.rstrip())
# obj.close()

number_files = len(files_in_dir)
dateTimeObj = datetime.now()

print("Analyse von ", number_files, " Dokument/en wird gestartet...")
#-----------------------------------
#--- EXTRACT TEXT FROM DOCUMENTS ---
#-----------------------------------

extracted_text = ''
for file in files_in_dir:
    #print("Analyse gestartet")
    fp = open(dir+file, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    parser.set_document(doc)
    #doc.set_parser(parser)
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

print("Analyse beendet")
#--------------------------------------------
#--- DELETE STOPWORDS FROM EXTRACTED TEXT ---
#--------------------------------------------

stop_words = set(stopwords.words('german')) 
stopword_extension = ['(', ')','.',':',',',';','!','?','´','"','“','„','»', '«', '–', '—','•'] 
stop_words.update(stopword_extension) # -- erweitert die Stoppwortliste


word_tokens = word_tokenize(extracted_text) 
  
filtered_sentence = [w for w in word_tokens if not w in stop_words] 
  
filtered_sentence = [] 
  
for w in word_tokens: 
    if w not in stop_words: 
        filtered_sentence.append(w) 
  
#----------------------------
#--- USE STEMMING ON TEXT ---
#----------------------------

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer('german')
stemmed_text = [stemmer.stem(word) for word in filtered_sentence]
#print(stemmed_text)

from collections import Counter
counts = Counter(stemmed_text)

#----------------------------------
#--- PRINT DURATION OF ANALYSIS ---
#----------------------------------

dateTimeObjEnd = datetime.now()

analyse_dauer = dateTimeObjEnd - dateTimeObj
print("Analysedauer: ", analyse_dauer)

#---------------------
#--- PLOTTING AREA ---
#---------------------

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.linspace(0, 20, 100)
plt.plot(x, np.cos(x))
plt.show()