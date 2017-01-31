import PyPDF2
pdfFileObj = open('SVR1.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pdfReader.numPages
