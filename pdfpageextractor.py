import PyPDF2, os
# Get all the PDF filenames.
pdfFiles = []
for filename in os.listdir('/Users/lmichaele/Documents/):
    if filename.endswith('.pdf'):
        pdfFiles.append(filename)
        pdfFiles.sort(key = str.lower)
pdfWriter = PyPDF2.PdfFileWriter()


# Loop through all the PDF files.
for filename in pdfFiles:
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# Loop through all the pages  and add them.
for pageNum in range(0, pdfReader.numPages):
    pageObj = pdfReader.getPage(pageNum)
    pdfWriter.addPage(pageObj)

pdfOutput = open('allminutes.pdf', 'wb')
    pdfWriter.write(pdfOutput)
    pdfOutput.close()
                           
