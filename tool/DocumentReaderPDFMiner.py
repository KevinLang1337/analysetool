from nltk.tokenize import word_tokenize

data_wordcloud = {}
data_temp = dict()
data_foamtree = {}


def get_data_foamtree():
    return data_foamtree


def get_data_temp():
    return data_temp


def get_data_wordcloud():
    return data_wordcloud


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
    from pdfminer.pdfinterp import resolve1
    from os import listdir
    from os.path import isfile, join
    from datetime import datetime
    import time
    from console_progressbar import ProgressBar

    dir = "tool/documents/"  # Directory to stored documents
    files_in_dir = [f for f in listdir(dir) if isfile(
        join(dir, f))]  # all files in the directory

    number_files = len(files_in_dir)  # amount of files in the directory

    pb = ProgressBar(total=100, prefix='Seiten zu ', suffix=' extrahiert',
                     decimals=0, length=50, fill='|', zfill='-')

    # time.sleep(5)

    print("Analyse von ", number_files, " Dokument/en wird gestartet...")

    dateTimeObj = datetime.now()  # first timestamp for the duration of the analysis

    list_of_tokens = []

    file_counter = 1
    # --- EXTRACT TEXT FROM DOCUMENTS ---
    for file in files_in_dir:
        print("#--- Dokument ", file_counter, ": ", file, " ---#")

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

            number_of_pages = resolve1(doc.catalog['Pages'])['Count']
            pb.print_progress_bar(100/number_of_pages*page_counter)
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

    useLDA(list_of_tokens, amount, files_in_dir)
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

    stop_words = set(stopwords.words('german'))  # model for german stopwords
    stopword_extension = ['(', ')', '.', ':', ',', ';', '!', '?', '´', '"', '“', '„', '»', '«',
                          '>', '<', '|', '–', '—', '_', '•', '...', '%', '!', '§', '!', '&', '/', '=', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\uf0b7', 'al', 'et', 'autor', 'sowie', 'müssen', 'aber']
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

    nlp = spacy.load('de_core_news_sm')  # model for german texts

    list_to_str = ' '.join(token for token in list_with_tokens)

    doc = nlp(list_to_str)

    lemmatized_text = " ".join([token.lemma_ for token in doc])
    word_tokens = word_tokenize(lemmatized_text)

    print("Lemmatisierung durchgeführt")
    return word_tokens

# --- LATENT DIRICHLET ALLOCATION ---


def useLDA(list_of_token, amount_topics, files_in_directory):

    import gensim
    from gensim import corpora, models
    dictionary = corpora.Dictionary(list_of_token)
    corpus = [dictionary.doc2bow(word) for word in list_of_token]

    default_amount_topics = 5
    minimum_probability = 0.10

    # IF NO AMOUNT IS PROVIDED
    if amount_topics == "":
        amount_topics = default_amount_topics

    # IF AMOUNT IS PROVIDED
    elif amount_topics != "":
        amount_topics = int(amount_topics)

    # IF AMOUNT IS PROVIDED BUT 0
    if amount_topics == 0:
        amount_topics = default_amount_topics

    # Main LDAModel
    ldamodel = gensim.models.ldamodel.LdaModel(
        corpus=corpus, num_topics=amount_topics, id2word=dictionary,
        passes=15, minimum_probability=minimum_probability)

    print("")
    print("#---- TOPICS ----#")

    prepareDataForFoamtree(amount_topics, files_in_directory, ldamodel, corpus)
    #prepareDataForWordcloud(ldamodel, corpus, 50)

    topics = ldamodel.show_topics(
        num_words=4, formatted=False)  # num_words = 4
    for topic in topics:
        print("###", topic)
        print("--------------------")

    return 0


def prepareDataForFoamtree(amount_topics, files_in_directory, ldamodel, corpus):
    import gensim
    from gensim import corpora, models

    # Create dictionary out of topics
    topic_dict = {k: [] for k in range(0, amount_topics)}
    for docID in range(len(files_in_directory)):
        topic_vector = ldamodel[corpus[docID]]

        for topicID, prob in topic_vector:
            print("'", files_in_directory[docID],
                  "' (", topicID, "/", prob, ")")

            temp_tuple = (docID, files_in_directory[docID], prob)
            topic_dict[topicID].append(temp_tuple)

        
    print("----------------------------")



    upper_group = []
    for key in sorted(topic_dict.keys()):
        if len(topic_dict[key]) > 0:
            # 0  ::  [(3, 'sample_deutsch.pdf', 0.99755144)]
            topic_title = "Topic "
            topic_title += str(key)
            middle_group = []
            upper_dict = {"label": topic_title, "groups": middle_group}
            # {"label":Topic 1}

            for docID, docTitle, prob in topic_dict[key]:

                middle_dict = {"label": docTitle}
                middle_group.append(middle_dict)

            upper_group.append(upper_dict)
            data_foamtree.update({"groups": upper_group})
    print("")


def prepareDataForWordcloud(ldamodel, corpus, amount_items):

    dictionary_keys = ldamodel.id2word

    temp_data = []
    for temp_corpus in corpus:
        for x in temp_corpus:
            temp_x = x
            temp_key = dictionary_keys[temp_x[0]]
            temp_value = temp_x[1]
            temp_tuple = (temp_key, temp_value)
            temp_data.append(temp_tuple)
            # data.update(temp_pair)

    temp_data = sort_tuple(temp_data)
    if len(temp_data) >= amount_items:
        data_wordcloud.update(dict(temp_data[0:amount_items]))
    elif len(temp_data) < amount_items:
        data_wordcloud.update(dict(temp_data[0:len(temp_data)]))

    return temp_data


def sort_tuple(tup):

    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst-i-1):
            if (tup[j][1] > tup[j + 1][1]):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp

    tup.reverse()
    return tup
