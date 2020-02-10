from nltk.tokenize import word_tokenize
data_wordcloud = {}
data_temp = dict()
data_foamtree = {}
amount_processed_documents = int()

def get_data_foamtree():
    return data_foamtree


def get_data_temp():
    return data_temp


def get_data_wordcloud():
    return data_wordcloud

def get_amount_processed_documents():
    return amount_processed_documents

def process_pdf(amount, date_from, date_until, file_ids):
    print(amount)
    print(date_from)
    print(date_until)

    from datetime import datetime
    from console_progressbar import ProgressBar
    from .models import Document
    import codecs

    documents_in_dir = []

    print("File_IDs", file_ids)

    for id in file_ids:
        id = int(id)
        doc = Document.objects.get(id=id)
        documents_in_dir.append(doc)

    number_files = len(documents_in_dir)  # amount of files in the directory

    pb = ProgressBar(total=100, prefix='Seiten zu ', suffix=' extrahiert',
                     decimals=0, length=50, fill='|', zfill='-')

    # time.sleep(5)

    print("Analyse von ", number_files, " Dokument/en wird gestartet...")

    dateTimeObj = datetime.now()  # first timestamp for the duration of the analysis

    list_of_tokens = []

    file_counter = 1
    # --- EXTRACT TEXT FROM DOCUMENTS ---
    for document in documents_in_dir:
        extracted_text = ''
        if document.extension == ".pdf":
            print("#--- Dokument ", file_counter, ": ", document, " ---#")
            extracted_text = extractTextFromPDF(document, pb, extracted_text)

        elif document.extension == ".txt":  

           
            print("#--- Dokument ", file_counter, ": ", document, " ---#")
            # Open the file with read only permit
            # Try to open file with different encodings
            # -- UTF-8
            try:
                f = codecs.open("media/"+str(document.file), "r", 'utf-8') # TODO: Stürzt ab, wenn Dokument nicht utf-8 ist
                extracted_text = f.readlines()
                f.close()
                print("Decoding für utf-8 angewendet.")
            except:
                # -- UTF-16
                try:
                    f = codecs.open("media/"+str(document.file), "r", 'utf-16') # TODO: Stürzt ab, wenn Dokument nicht utf-8 ist
                    extracted_text = f.readlines()
                    f.close()
                    print("Decoding für utf-16 angewendet.")
                except:
                    # -- latin1
                    try:
                        f = codecs.open("media/"+str(document.file), "r", 'latin1') # TODO: Stürzt ab, wenn Dokument nicht utf-8 ist
                        extracted_text = f.readlines()
                        f.close()
                        print("Decoding für latin1 angewendet.")
                    except:
                        print("Es konnte kein passendes Format für Decoding gefunden werden. Dokument wird ignoriert!")
            
        else:
            print("")
            print("##### Warnung ####")    
            print("Dokumentenendung "+str(document.extension)+" unbekannt.")
            print("##################")
            print("")    
            documents_in_dir.remove(document)

        if (extracted_text != ''):
            
            text_without_numbers = removeNumbers(extracted_text)
            detected_language = languageDetection(text_without_numbers)
            print("Sprache erkannt: ", detected_language)
            text_without_stopwords = removeStopwords(text_without_numbers, detected_language)
            lemmatized_tokens = lemmatizeTokens(text_without_stopwords, detected_language)
            list_of_tokens.append(lemmatized_tokens)
            print("Anzahl Einträge: ", len(lemmatized_tokens))
            print("##-------------------------------------------##")
            print("")
            file_counter += 1
           
    # Set amount of processed documents       
    global amount_processed_documents 
    amount_processed_documents = file_counter-1
    print("Anzahl Dokumente: ", amount_processed_documents)
    print("Anzahl Dokumente2: ", file_counter)
    # --- PRINT DURATION OF ANALYSIS ---
    if len(list_of_tokens) !=  0:
        useLDA(list_of_tokens, amount, documents_in_dir)
    else:
            print("Es konnte keine Analyse durchgeführt werden.")
            print("") 
    dateTimeObjEnd = datetime.now()
    analyse_dauer = dateTimeObjEnd - dateTimeObj

    print("Analyse beendet")
    print("Analysedauer: ", analyse_dauer)

def extractTextFromPDF(document, progressbar, extracted_text):
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import PDFPageAggregator
    from pdfminer.layout import LAParams, LTTextBox, LTTextLine
    from pdfminer.pdfinterp import resolve1

    fp = open("media/"+str(document.file), 'rb')
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
        progressbar.print_progress_bar(100/number_of_pages*page_counter)
        page_counter += 1
    return extracted_text

# --- DELETE NUMBERS FROM EXTRACTED TEXT -----


def removeNumbers(lemmatized_text):
    temp_text = ''.join(c for c in lemmatized_text if not c.isdigit())
    print("Zahlen wurden entfernt")
    return temp_text

# --- DELETE STOPWORDS FROM EXTRACTED TEXT ---
def removeStopwords(text, language):

    from spacy.lang.en import English
    from spacy.lang.de import German

    # Load German tokenizer, tagger, parser, NER and word vectors
    if language == 'de':
        nlp = German()
        doc = nlp(text)

        # Create list of word tokens
        token_list = []
        for token in doc:
            token_list.append(token.text)

        from spacy.lang.de.stop_words import STOP_WORDS
        # Create list of word tokens after removing stopwords
        filtered_sentence = []

        for word in token_list:
            lexeme = nlp.vocab[word]
            if lexeme.is_stop == False and \
                lexeme.is_punct == False and \
                lexeme.is_space == False and \
                lexeme.is_bracket == False and \
                lexeme.is_quote == False and \
                lexeme.like_url == False and \
                lexeme.like_email == False and \
                len(word) > 3:
                    filtered_sentence.append(word)

        return filtered_sentence

    # Load English tokenizer, tagger, parser, NER and word vectors
    elif language == 'en':
        nlp = English()
        doc = nlp(text)

        # Create list of word tokens
        token_list = []
        for token in doc:
            token_list.append(token.text)

        from spacy.lang.en.stop_words import STOP_WORDS
        # Create list of word tokens after removing stopwords
        filtered_sentence = []

        for word in token_list:
            lexeme = nlp.vocab[word]
            if lexeme.is_stop == False and \
                lexeme.is_punct == False and \
                lexeme.is_space == False and \
                lexeme.is_bracket == False and \
                lexeme.is_quote == False and \
                lexeme.like_url == False and \
                lexeme.like_email == False and \
                len(word) > 3:
                    filtered_sentence.append(word)

        return filtered_sentence    

# --- USE LEMMATIZATION ON EXTRACTED TEXT ---
def lemmatizeTokens(list_with_tokens, language):
    import spacy
    from collections import Counter

    if language == 'de':
        nlp = spacy.load('de_core_news_sm')  # model for german texts
    elif language == 'en':
        nlp = spacy.load('en_core_web_sm')  # model for english texts

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

    # CREATE A DICTIONARY
    dictionary = corpora.Dictionary(list_of_token)
    # CREATE A CORPUS
    corpus = [dictionary.doc2bow(word) for word in list_of_token]

    # SETTINGS FOR LDA
    default_amount_topics = 5
    minimum_probability = 0.1

    # IF NO AMOUNT IS PROVIDED
    if amount_topics == "":
        amount_topics = default_amount_topics

    # IF AMOUNT IS PROVIDED
    elif amount_topics != "":
        amount_topics = int(amount_topics)

    # IF AMOUNT IS PROVIDED BUT 0
    if amount_topics == 0:
        amount_topics = default_amount_topics

    # Main model
    ldamodel = gensim.models.ldamodel.LdaModel(
        corpus=corpus, num_topics=amount_topics, id2word=dictionary,
        passes=1, minimum_probability=minimum_probability, callbacks=None)

    prepareDataForWordcloud(ldamodel, corpus, 50)

    topic_dict = {k: [] for k in range(0, amount_topics)}
    
    print("#------#")
    # SAVE DOCID AND DOCTITLE IN TOPIC_DICTIONARY
    for docID in range(len(files_in_directory)):
        topic_vector = ldamodel[corpus[docID]]
        file_temp = str(files_in_directory[docID])+str(files_in_directory[docID].extension)
        print("Doc ", docID, " (", file_temp,")")
        print("Vector: ", topic_vector)
        print("---")

        for topicID, probability in topic_vector:
            tuple_temp = (docID, file_temp)
            topic_dict[topicID].append(tuple_temp)

    print(" # # # # # # # # # # # # # ")
    # CREATE NEW CORPUS FROM SUBCORPORA
    upper_group = []
    for topicID in topic_dict:
        
        topic_dict_sub = {k: [] for k in range(0, amount_topics)}
        
        if len(topic_dict[topicID]) > 0:
            print(" ")
            print("#-------------#", len(topic_dict[topicID]))
            print("### Maintopic ", topicID,": ", topic_dict[topicID])
            
            # CREATE LABEL FOR FOAMTREE
            main_topic = ldamodel.show_topic(topicID, 5)

            topic_title = "Topic: ["
            title_text = ""

            for item in main_topic:
                title_text += item[0]
                title_text += ", "
            title_text = title_text[:-2]

            topic_title += title_text
            topic_title += "]"

            middle_group = []
            upper_dict = {"id": topicID
            , "label": topic_title,
                          "groups": middle_group}
            upper_group.append(upper_dict)

            new_corpus = []
            for tuple_doc in topic_dict[topicID]:
                new_corpus.append(corpus[tuple_doc[0]])

            print(" - - -")
            # Sub model of this topic
            ldamodel_sub = gensim.models.ldamodel.LdaModel(
                corpus=new_corpus, num_topics=amount_topics, id2word=dictionary,
                passes=1, minimum_probability=minimum_probability, callbacks=None)        
            
            for tuple_doc in topic_dict[topicID]:
                docID = tuple_doc[0]
                docTitle = tuple_doc[1]
                print("---------------------------------------------")
                print("DocID ", docID, " (", docTitle,")")
                topic_vector_sub = ldamodel_sub[corpus[tuple_doc[0]]]
                print("Vector_Sub: ", topic_vector_sub) 

                for topicID, probability in topic_vector_sub:
                    tuple_temp = (docID, docTitle)
                    topic_dict_sub[topicID].append(tuple_temp)

                print("---------------------------------------------")

        for topicID_sub in topic_dict_sub:
            
            if len(topic_dict_sub[topicID_sub]) > 0:
                print("Subtopic ", topicID_sub,": ", topic_dict_sub[topicID_sub])

                sub_topic = ldamodel_sub.show_topic(topicID_sub, 5)

                topic_title = "Subtopic: ["
                title_text = ""

                for item in sub_topic:
                    title_text += item[0]
                    title_text += ", "
                title_text = title_text[:-2]

                topic_title += title_text
                topic_title += "]"

                document_group = []
                middle_dict = {"id": topicID_sub
                , "label": topic_title,
                            "groups": document_group}
                middle_group.append(middle_dict)

                for tuple_doc in topic_dict_sub[topicID_sub]:
                    docID = tuple_doc[0]
                    docTitle = tuple_doc[1]
                    document_dict = {"id":docID, "label":docTitle}
                    document_group.append(document_dict)    
        
    data_foamtree.update({"groups": upper_group})
    return ldamodel


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


def languageDetection(text):
    import spacy
    from spacy_langdetect import LanguageDetector

    nlp = spacy.load('de_core_news_sm')
    nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)
    # text = 'This is an english text.'
    doc = nlp(text)
    # document level language detection. Think of it like average language of the document!
    language = doc._.language['language']
    return language
