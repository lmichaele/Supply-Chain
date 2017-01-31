import glob
import os
import sys
import csv
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1

#input file path for specific file
#filename = "C:\Users\edwluk5\AppData\Local\Programs\Python\Python35-32\SVR1.pdf"
#fp = open(filename, 'rb')

#open new csv file
out_file ='C:\Users\edwluk5\AppData\Local\Programs\Python\Python35-32\output.csv', 'w+'
writer = csv.writer(out_file)
#header row
writer.writerow(('Name coordinator', 'Date', 'Address', 'District',
                 'City', 'Complaintnr'))

path ='C:\Users\edwluk5\AppData\Local\Programs\Python\Python35-32\SVR1.pdf'
for filename in glob.glob(os.path.join(path, '*.pdf')):
    fp = open(filename, 'rb')
    #read pdf's
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    #doc.initialize()    # <<if password is required
    fields = resolve1(doc.catalog['AcroForm'])['Fields']
    row = []
    for i in fields:
        field = resolve1(i)
        name, value = field.get('T'), field.get('V')
        row.append(value)
    writer.writerow(row)

out_file.close()
