
def getDateFromDocument(document):
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument

    fp = open("media/"+str(document.file), 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    pdf_creation_date = doc.info[0]["CreationDate"]
    
    return(convertDatetimePDF(pdf_creation_date))

def convertDatetimePDF(date):
    from datetime import datetime
    dtformat = "%Y%m%d%H%M%S"
    clean = date.decode("utf-8").replace("D:","").split('+')[0]
    obj_date = datetime.strptime(clean, dtformat) 
    
    return (datetime.strftime(obj_date,'%Y-%m-%d'))   
    