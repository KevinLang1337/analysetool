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
        passes=15, minimum_probability=minimum_probability, callbacks=None)

    print("")
    print("#---- TOPICS ----#")

    prepareDataForFoamtree(
        amount_topics, files_in_directory, ldamodel, corpus, dictionary)
    prepareDataForWordcloud(ldamodel, corpus, 50)

    topics = ldamodel.show_topics(
        num_words=4, formatted=False)  # num_words = 4
    for topic in topics:
        print("### Topic", topic)
        print("--------------------")

    return 0


def prepareDataForFoamtree(amount_topics, files_in_directory, ldamodel, corpus, dictionary):
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

    # #---- TOPICS ----#
    # ' Anforderungen Masterarbeit - Kopie.pdf ' ( 2 / 0.9968493 )
    # ' Anforderungen Masterarbeit.pdf ' ( 2 / 0.9968493 )
    # ' sample.pdf ' ( 3 / 0.993043 )
    # ' sample_deutsch.pdf ' ( 1 / 0.99755144 )

    print("----------------------------")

    upper_group = []

    sub_dict = {k: [] for k in range(0, amount_topics)}

    for key in sorted(topic_dict.keys()):
        if len(topic_dict[key]) > 0:

            topic_title = "Topic: ["
            topics = ldamodel.show_topic(key, 5)
            title_text = ""

            for item in topics:
                title_text += item[0]
                title_text += ", "
            title_text = title_text[:-2]

            topic_title += title_text
            topic_title += "]"
            middle_group = []

            upper_dict = {"id": key, "label": topic_title,
                          "groups": middle_group}
            upper_group.append(upper_dict)
            # {"label":Topic 1}

            for docID, docTitle, prob in topic_dict[key]:
                sub_tuple = (docID, docTitle, corpus[docID])
                sub_dict[key].append(sub_tuple)









    
    # SUB-TOPIC
    for key in sub_dict.keys():
        topic_dict_sub = {k: [] for k in range(0, amount_topics)}
        middle_group = []
        print("Maintopic: ", key)

        new_key = sub_dict[key]

        if (len(new_key) > 0):

            list_of_docs = []
            list_of_corpora = []
            new_corpus = []

            for element in new_key:

                docID = element[0]
                docTitle = element[1]
                corpus_sub = element[2]

                tuple_doc = (docID, docTitle)
                list_of_docs.append(tuple_doc)
                list_of_corpora.append(corpus_sub)
                new_corpus += corpus_sub
                print("DocID: ", docID)
                print("DocTitle: ", docTitle)
                print("----------")

            if(len(list_of_corpora) > 0):

                ldamodel_sub = gensim.models.ldamodel.LdaModel(
                    corpus=list_of_corpora, num_topics=amount_topics, id2word=dictionary,
                    passes=15, minimum_probability=0.10, callbacks=None)

            for file_temp in list_of_docs:

                (docID, docTitle) = file_temp
                
                topic_vector_sub = ldamodel_sub[corpus[docID]]

            document_group = []
            for topicID, prob in topic_vector_sub:
                print("MainTopic", key, "'", files_in_directory[docID],
                    "' (", topicID, "/", prob, ")")

                temp_tuple = (docID, files_in_directory[docID], prob)
                topic_dict_sub[topicID].append(temp_tuple)

                print("### Element Topic ", key, " / Subtopic ", topicID, " ###: ", topic_dict_sub[topicID])
                
                topic_title = "Subtopic: ["
                topics = ldamodel_sub.show_topic(topicID, 5)
                title_text = ""

                for item in topics:
                    title_text += item[0]
                    title_text += ", "
                title_text = title_text[:-2]
                topic_title += title_text
                topic_title += "]"
                print(topic_title)
                middle_dict = {"label":topic_title, "groups": document_group}
                middle_group.append(middle_dict)

                document_dict = {"label": files_in_directory[docID]}
                document_group.append(document_dict)
                


                # topics = ldamodel_sub.show_topics(
                # num_words=4, formatted=False)  # num_words = 4
                # for topic in topics:
                #     print("### Subtopic", topic)
                #     print("--------------------")

        print(" # # # # # # # # # ")
        print("")

        for upper_dict in upper_group:

                if key == upper_dict['id']:
                    upper_dict['groups'] = middle_group 
        
        
        #     document_group = []

        #     middle_dict = {"id": key, "label": topic_title,
        #                   "groups": document_group}
        #     middle_group.append(middle_dict)
        #     # {"label":Topic 1}

        # for upper_dict in upper_group:

        #         if key == upper_dict['id']:
        #             upper_dict['groups'] = middle_group    

    
    # for key in sorted(topic_dict_sub.keys()):
    #     if len(topic_dict_sub[key]) > 0:

    #         topic_title = "Topic " + str(key) + ": ["
    #         topics = ldamodel_sub.show_topic(key, 5)
    #         title_text = ""

    #         for item in topics:
    #             title_text += item[0]
    #             title_text += ", "
    #         title_text = title_text[:-2]

    #         topic_title += title_text
    #         topic_title += "]"
    #         middle_group = []

    #         upper_dict = {"id": key, "label": topic_title,
    #                       "groups": middle_group}
    #         upper_group.append(upper_dict)
    #         # {"label":Topic 1}

    #         for docID, docTitle, prob in topic_dict[key]:
    #             sub_tuple = (docID, docTitle, corpus[docID])
    #             sub_dict[key].append(sub_tuple)


    # for key in sub_dict.keys():

    #     new_key = sub_dict[key]

    #     list_of_docs = []
    #     list_of_corpora = []

    #     for element in new_key:
    #         document = element[1]
    #         corpus_temp = element[2]

    #         docID_docTitle = (docID, docTitle)
    #         list_of_docs.append(docID_docTitle)
    #         list_of_corpora.append(corpus_temp)

    #     if(len(list_of_corpora) > 0):
    #         # perform LDA on sub_corpus
    #         print("LIST OF DOCS: ", list_of_docs)
    #         middle_group = createLDASubModel(list_of_corpora, amount_topics, dictionary, list_of_docs, corpus, files_in_directory)

    #         for upper_dict in upper_group:

    #             if key == upper_dict['id']:
    #                 upper_dict['groups'] = middle_group

    # upper_dict['groups'] = middle_group
    data_foamtree.update({"groups": upper_group})

    print("")


def createLDASubModel(sub_corpus, amount_topics, dictionary, files_in_sub_corpus, corpus, files_in_directory):
    import gensim

    print("###################")
    print("Sub_corpus: ", sub_corpus)
    print("Anzahl: ", amount_topics)
    print("Dic: ", dictionary)
    print("Files sub: ", files_in_sub_corpus)
    print("Files: ", files_in_directory)

    # perform LDA on sub_corpus
    ldamodel = gensim.models.ldamodel.LdaModel(
        corpus=sub_corpus, num_topics=amount_topics, id2word=dictionary,
        passes=15, minimum_probability=0.10, callbacks=None)

    # Create dictionary out of topics
    sub_topic_dict = {k: [] for k in range(0, amount_topics)}

    for file_temp in files_in_sub_corpus:
        (docID, docTitle) = file_temp
        topic_vector = ldamodel[corpus[docID]]

        for topicID, prob in topic_vector:

            temp_tuple = (docID, files_in_directory[docID], prob)
            sub_topic_dict[topicID].append(temp_tuple)

    middle_group = []

    for key in sorted(sub_topic_dict.keys()):
        if len(sub_topic_dict[key]) > 0:

            sub_topic_title = "Topic "
            sub_topic_title += str(key)
            sub_topic_title += ": ["
            test = ldamodel.show_topic(key, 5)
            title_text = ""

            for item in test:
                title_text += item[0]
                title_text += ", "
            title_text = title_text[:-2]

            sub_topic_title += title_text
            sub_topic_title += "]"

            document_group = []

            middle_dict = {"label": sub_topic_title, "groups": document_group}
            middle_group.append(middle_dict)

            print(" #### KEY ", key, " ####")
            for document_tuple in sub_topic_dict[key]:
                print("DOCUMENT TUPLE: ", document_tuple)
                docID = document_tuple[0]
                docTitle = document_tuple[1]

                document_dict = {"label": docTitle}
                document_group.append(document_dict)

    return middle_group


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
