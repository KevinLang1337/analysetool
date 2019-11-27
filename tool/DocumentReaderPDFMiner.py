from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

from os import listdir
from os.path import isfile, join
 
dir = 'C:/Users/lanki/Documents/Uni/Semester 4/Masterarbeit/Test-Daten/funktionsfähig/'
files_in_dir = [f for f in listdir(dir) if isfile(join(dir, f))]
print (files_in_dir)


# obj = open('C:/Users/lanki/Documents/Uni/Semester 4/Masterarbeit/Test-Daten/Funktionsfähig/ipsum.txt', encoding="utf8")
# for line in obj:
#     print(line.rstrip())
# obj.close()

#-------------------

#-------------------


# #fp = open('../Testdatei.pdf', 'rb')

number_files = len(files_in_dir)
print("Analyse von ", number_files, " Dokument/en wird gestartet...")



extracted_text = ''
for file in files_in_dir:
    print("Analyse gestartet")
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
print(extracted_text)