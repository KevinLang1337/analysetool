from nltk.tokenize import word_tokenize

def process_pdf(amount, date_from, date_until):
    print(amount)
    print(date_from)
    print(date_until)
   
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import PDFPageAggregator
    from pdfminer.layout import LAParams, LTTextBox, LTTextLine
    from os import listdir
    from os.path import isfile, join
    from datetime import datetime
    import time
    from console_progressbar import ProgressBar

    
    dir = "tool/documents/" # Directory to stored documents
    files_in_dir = [f for f in listdir(dir) if isfile(join(dir, f))] # all files in the directory
    
    number_files = len(files_in_dir) # amount of files in the directory

    # pb = ProgressBar(total=100, prefix='Analyse', suffix='', decimals=2, length=50, fill='|', zfill='-')
    # pb.print_progress_bar(2)
    # time.sleep(5)

    print("Analyse von ", number_files, " Dokument/en wird gestartet...")

    dateTimeObj = datetime.now() # first timestamp for the duration of the analysis

    list_of_tokens = []

    file_counter = 1
    # --- EXTRACT TEXT FROM DOCUMENTS ---
    for file in files_in_dir:
        print("#--- Dokument ", file_counter, " ---#")
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

        page_counter = 1
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    extracted_text += lt_obj.get_text()

            print("Seite ", page_counter, " extrahiert")
            page_counter += 1  
                    
        text_without_numbers = removeNumbers(extracted_text)
        text_without_stopwords = removeStopwords(text_without_numbers)
        lemmatized_tokens = lemmatizeTokens(text_without_stopwords)
        list_of_tokens.append(lemmatized_tokens)
        print("Anzahl Einträge: ", len(lemmatized_tokens))
        print("##-------------------------------------------##")
        print("")
        file_counter += 1

    
    # --- PRINT DURATION OF ANALYSIS ---
    dateTimeObjEnd = datetime.now()
    analyse_dauer = dateTimeObjEnd - dateTimeObj
    
    
    print("Anzahl: ", amount)

    useLDA(list_of_tokens, amount)
    print("Analyse beendet")
    print("Analysedauer: ", analyse_dauer)
        
# --- DELETE NUMBERS FROM EXTRACTED TEXT -----
def removeNumbers(lemmatized_text):
    temp_text = ''.join(c for c in lemmatized_text if not c.isdigit())
    print("Zahlen wurden entfernt")
    return temp_text

# --- DELETE STOPWORDS FROM EXTRACTED TEXT ---   
def removeStopwords(lemmatized_text):
    import nltk
    from nltk.corpus import stopwords
    

    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

    stop_words = set(stopwords.words('german')) # model for german stopwords
    stopword_extension = ['(', ')', '.', ':', ',', ';', '!', '?', '´', '"', '“', '„', '»', '«',
                        '>', '<', '|', '–', '—', '_', '•', '...', '%', '!', '§', '!', '&', '/', '=', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\uf0b7', 'al', 'et', 'autor']
    stop_words.update(stopword_extension)  # expands the list of stopwords

    word_tokens = word_tokenize(lemmatized_text) 

    filtered_text = []

    # IF WORDS ARE NOT STOPWORD AND HAVE MORE CHARACTER THAN 3
    for w in word_tokens:
        if w not in stop_words and len(w) > 3:
            filtered_text.append(w)

    print("Stoppwörter wurden entfernt")
    return filtered_text

# --- USE LEMMATIZATION ON EXTRACTED TEXT ----
def lemmatizeTokens(list_with_tokens):
    import spacy
    from collections import Counter

    nlp = spacy.load('de_core_news_sm') # model for german texts
   
    list_to_str = ' '.join(token for token in list_with_tokens)

    doc = nlp(list_to_str)
    
    lemmatized_text = " ".join([token.lemma_ for token in doc])
    word_tokens = word_tokenize(lemmatized_text) 
    
    print("Lemmatisierung durchgeführt")
    return word_tokens

# --- LATENT DIRICHLET ALLOCATION ---
def useLDA(list_of_token, amount_topics):

    # https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html
    # TODO: Stopwords, Stemming usw. für jedes Dokument einzeln machen. Dann die Liste mit Token einer anderen Liste hinzufügen
    # from gensim import corpora, models

    # dictionary = corpora.Dictionary(filtered_text)
    # corpus = [dictionary.doc2bow(lemmatized_text) for lemmatized_text in filtered_text]
    # print(corpus[0])
    import gensim
    from gensim import corpora, models
    dictionary = corpora.Dictionary(list_of_token)
    corpus = [dictionary.doc2bow(word) for word in list_of_token]

    default_amount_topics = 3

    # IF NO AMOUNT IS PROVIDED
    if amount_topics == "":
        amount_topics = int(0)
    # IF AMOUNT IS PROVIDED    
    elif amount_topics != "":
        amount_topics = int(amount_topics)

    if amount_topics == 0:
        print("keine Anzahl angegeben")
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=default_amount_topics, id2word = dictionary, passes=1)

    elif amount_topics > 0:
        print("Anzahl ", amount_topics, " angegeben!")
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=amount_topics, id2word = dictionary, passes=1)
    
    print("")
    print("#---- TOPICS ----#")
    return ldamodel.print_topics(num_topics=amount_topics, num_words=10)