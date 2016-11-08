#! python3
#PDF TO CSV

import os, PyPDF2, csv, re, shutil, send2trash

pdfFiles = []

os.chdir('G:\\Supply Chain\\Warehouse\\Stocktake\\Stocktake Variance Reports')

for filename in os.listdir('.'):
    if filename.endswith('.pdf'):
        pdfFiles.append(filename)
        
pdfFiles.sort(key = str.lower)

pdfWriter = PyPDF2.PdfFileWriter()

Allpdf = []

for filename in pdfFiles:
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    for pageNum in range(0, pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

pdfOutput = open('master.pdf', 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()

pdfFileObj2 = open('master.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj2)

LastPage = (pdfReader.numPages)-1 
CurrentPage = 0
AllPdfText = []
while CurrentPage <= LastPage :
    pageObj = pdfReader.getPage(CurrentPage)
    PdfText = pageObj.extractText()
    AllPdfText.append(str(PdfText)) 
    CurrentPage = CurrentPage + 1

AllPagesStr = ''.join(AllPdfText)

PhysInvReg =  re.compile(r'1200\d\d\d\d\d')
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

pdfFileObj2.close()
csvoutput.close()

#send2trash.send2trash('G:\\Supply Chain\\Warehouse\\Stocktake\\Stocktake Variance Reports\\master.pdf')# Delete the master  pdf

#TODO move all pdfs into archives

source = 'G:\\Supply Chain\\Warehouse\\Stocktake\\Stocktake Variance Reports'
dest1 = 'G:\\Supply Chain\\Warehouse\\Stocktake\\Variance Archives'

files = os.listdir(source)

for f in files: 
    if filename.endswith('.pdf'):
        shutil.move(f, dest1)



