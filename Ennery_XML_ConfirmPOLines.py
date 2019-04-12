#! /usr/bin/python

import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import re, csv, os, shutil, xlsxwriter
from datetime import timedelta, datetime
import pandas as pd

tkroot = tk.Tk()
tkroot.withdraw()
file = filedialog.askopenfilename()
directory = os.path.dirname(file)
 
tree = ET.parse(file)
root = tree.getroot()
xmlstr = ET.tostring(root, encoding='utf8', method='xml')
 
ln = re.findall(r'<LineNumber>(\d*)</LineNumber>', (str(xmlstr)))
 
inv = re.findall(r'<InvoiceNumber>(........)', (str(xmlstr)))
 
pnol = re.findall(r'<PartNumberOrdered>([^<]+)</PartNumberOrdered>', (str(xmlstr)))
 
pnsl = re.findall(r'<PartNumberSupplied>([^<]+)</PartNumberSupplied>', (str(xmlstr)))
df = pd.DataFrame(dict(A=(pnsl)))
df.A = df.A.apply('="{}"'.format)

qtys = re.findall(r'<QuantitySent>(\d*)</QuantitySent>', (str(xmlstr)))

price = re.findall(r'<UnitPrice>([^<]+)</UnitPrice>', (str(xmlstr)))

orderref = re.findall(r'</OrderCategory><CustomerOrderRef>([^<]+)</CustomerOrderRef>', (str(xmlstr)))

dateissue = re.findall(r'<DateOfIssue>(\d{8})</DateOfIssue>', (str(xmlstr)))

partdiff = [i for i, j in zip(pnol, pnsl) if i != j]
if not partdiff:
    print("All parts match original order.")
else: print("Parts different from original PO (check validity in M3);"+(str(partdiff)))

### PO's to charge out 
cpos = ['3006869', '3006870', '3006875', '3006883', '3006968', '3006975',
        '3007071WGS', '3007111', '4009494', '3007134', '4009515', '3007166',
        '4009529', '4009530', '3007203', '3007340']

csvRows = []
csvRows2 = []
dcsvRows = []
n = 0
while n < len(ln): 
    partsupd = (str(pnsl[n])).replace(" ","")
    partsup = (df.A[n].replace(" ",""))
    qty = qtys[n]
    prc = price[n]
    po = orderref[n]
    doi = dateissue[0]
    if pnsl.count(pnsl[n]) > 1:
        Count = "TRUE"
    else:
        Count = "FALSE"
    if not po.isnumeric():
        print("Warning: Check Purchase Order Reference "+po)
    if po in cpos:
        print(po+" to be charged elsewhere")
    date = (datetime.now() + timedelta(days=7)).strftime("%Y%m%d")
    today = (datetime.now().strftime("%Y%m%d"))
    calc = (float(qty)) * (float(prc))
    row = ((', '.join(inv)),partsup,qty,prc,po,date,calc,Count,doi)
    drow = ((', '.join(inv)),partsupd,qty,prc,po,date,calc,Count)
    if po.startswith('300'):
        afrow = (partsup, qty, po, today)
        csvRows2.append(afrow)
    csvRows.append(row)
    dcsvRows.append(drow)
    
    n = n+1

csvRows.sort()

newrows = []
n=1
k=2
o=3
newrows.append(csvRows[0])
for row in csvRows:
    try:
        if csvRows[k][1]+csvRows[k][4] == csvRows[n][1]+csvRows[n][4]:
            newrow = (csvRows[n][0],csvRows[n][1],int(csvRows[n][2])+int(csvRows[k][2]),csvRows[n][3],csvRows[n][4],csvRows[n][5]) #Add n+1 in to skip over the line
            n=n+1
            k=k+1
        else: newrow = (csvRows[n])
        newrows.append(newrow)
        n=n+1
        k=k+1
    except IndexError:
        continue

outputfile = open('ConfirmPOLines.csv', 'a', newline='')
outputwriter = csv.writer(outputfile, dialect='excel')
for row in csvRows:
    outputwriter.writerow(row)
outputfile.close()

outputfile2 = open('//agsufs01/Supply/Replenishment/AF Frequency Review/Ennery_AF_Frequency.csv', 'a', newline='')
outputwriter2 = csv.writer(outputfile2, dialect='excel')
for row in csvRows2:
    outputwriter2.writerow(row)
outputfile2.close()

r = 0
c = 0


outputfile = open('//agsufs01/Supply/Python/Dissection_Invoice.csv', 'a', newline='')
outputwriter = csv.writer(outputfile, dialect='excel')
for row in csvRows:
    outputwriter.writerow(row)
outputfile.close()

shutil.move(file,'//agsufs01/Supply/Python/Invoice Archives/')
