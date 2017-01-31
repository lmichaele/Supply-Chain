import glob
import os
import sys
import csv
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1

#input file path for specific file
#filename = "C:\Python27\Scripts\MH_1.pdf"
#fp = open(filename, 'rb')

#open new csv file
out_file=open('C:\Users\Wonen\Downloads\Test\output.csv', 'w+')
writer = csv.writer(out_file)
#header row
writer.writerow(('Name coordinator', 'Date', 'Address', 'District',
                 'City', 'Complaintnr'))

#enter folder path to open multiple files
path = 'C:\Users\Wonen\Downloads\Test'
for filename in glob.glob(os.path.join(path, '*.pdf')):
    fp = open(filename, 'rb')
    #read pdf's
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    #doc.initialize()    # <<if password is required
    fields = resolve1(doc.catalog['AcroForm'])['Fields']
    for i in fields:
        field = resolve1(i)
        name, value = field.get('T'), field.get('V')
        print '{0}: {1}'.format(name, value)
        writer.writerow(value)
