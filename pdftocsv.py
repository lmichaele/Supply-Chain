#! python3
#PDF TO CSV PYTHON
#1)pulls a string of text of the whole pdf
#2)pulls a list of values from the text, #being line,part
#3)
#4)

import os
import PyPDF2
import csv
import re

#need to turn all the pdfs into one, then turn that into a string 

os.chdir('/Users/lmichaele/Documents/SVR/') 
os.getcwd()

pdfFiles = []

files = [f for f in os.listdir('.') if os.path.isfile(f)] #now you have a list of files.
for f in files:
    if f.endswith('.pdf'):
        pdfFiles.append(f)
        
pdfFiles.sort(key = str.lower)

Allpdf = []

for filename in pdfFiles:
    pdfFileObj = open(f, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    Allpdf.append(str(pdfReader))
    
#       pdfFileObj = open(f, 'rb') #fixprint me
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

pdfWriter = PyPDF2.PdfFileWriter()

for pageNum in range(0, len.Allpdf):
    pageObj = pdfReader.getPage(pageNum) #'PageObject' object has no attribute 'seek'
    append.pdfWriter(pageObj)

pdfReader = PyPDF2.PdfFileReader(pageObj)

LastPage = (pdfReader.numPages)-1 #there is a better way to do this but it works...
CurrentPage = 0
AllPdfText = []
while CurrentPage <= LastPage :
    pageObj = pdfReader.getPage(CurrentPage)
    PdfText = pageObj.extractText()
    AllPdfText.append(str(PdfText)) #how to change global things locally. 
    CurrentPage = CurrentPage + 1

AllPagesStr = ''.join(AllPdfText)

PhysInvReg =  re.compile(r'12000\d\d\d\d')
PhysInvNo = PhysInvReg.findall(AllPagesStr)

LineReg = re.compile(r'0000[1-9][0-1][0-9]')
LineNumbers = LineReg.findall(AllPagesStr)

PartIDreg = re.compile(r'0000[1-9][0-1][0-9]([0123456789SP.][0123456789SP.]+)')
PartID = PartIDreg.findall(AllPagesStr)

LocReg = re.compile(r'0000[1-9][0-1][0-9][0123456789SP.][0123456789SP.]+(\w\S+)')
Locations = LocReg.findall(AllPagesStr)

PartIDLocreg = re.compile(r'0000[1-9][0-1][0-9](...\d+\w......)')
PartIDLoc = PartIDLocreg.findall(AllPagesStr)

Countqtyreg = re.compile(r'(.{8}).{20}[S][VNQW][IWLA]')
countqty = Countqtyreg.findall(AllPagesStr)

SOHqtyreg = re.compile(r'(.{8}).{10}[S][VNQW][IWLA]')
SOHqty = SOHqtyreg.findall(AllPagesStr)

Diffqtyreg = re.compile(r'(......)[S][VNQW][IWLA]')
Diffqty = Diffqtyreg.findall(AllPagesStr)

Amount1reg = re.compile(r'.2\s\s.(...\d\.\d\d\d\d)\s\s')
amount1 = Amount1reg.findall(AllPagesStr)

Amount2reg = re.compile(r'.2\s\s....\d\.\d\d\d\d\s\s(.{11})')
amount2 = Amount2reg.findall(AllPagesStr)

Diffamountreg = re.compile(r'.2\s\s....\d\.\d\d\d\d\s\s.{13}(.{9})')
diffamount = Diffamountreg.findall(AllPagesStr)

csvoutput = open('csvoutput.csv', 'a', newline='')
outputWriter = csv.writer(csvoutput) 
length_list=len(LineNumbers)

i=0
while i!=length_list :
    data= LineNumbers[i],PartID[i],Locations[i],countqty[i],amount1[i],SOHqty[i],amount2[i],Diffqty[i],diffamount[i]
    i=i+1
    outputWriter.writerow(data)

csvoutput.close()
