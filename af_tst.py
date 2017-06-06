#! python3
#PDF-text TO CSV

import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import re, csv, os, shutil
from datetime import timedelta, datetime
import pandas as pd

tkroot = tk.Tk()
tkroot.withdraw()
file = filedialog.askopenfilename()
directory = os.path.dirname(file)

with open(file, 'r') as invoice:
	data=invoice.read()

invr = re.compile(r'(A0\d{6})')
invoicer = invr.findall(data)

Partr =  re.findall(r'[WXD]\d{7}(.*)\s.*[2-4]0[0-7]\d{4}\s\d\d\d[.]\d\d\d', (data))
df = pd.DataFrame(dict(A=(Partr)))
df.A = df.A.apply('="{}"'.format)

qrg = re.compile(r'CST\D*(\d*)')
qtyr = qrg.findall(data)

prg = re.compile(r'CST\D*\d*\s\d*\s(\d*[.]\d{4})')
prr = prg.findall(data)

Porg =  re.compile(r'([2-4]0[0-7]\d{4})\s\d\d\d[.]\d\d\d')
por = Porg.findall(data)

csvRows = []
n=0
x=-1
while n < len(Partr):
    Part = (df.A[n].replace(" ", ""))
    Qty = qtyr[n]
    Price = prr[n]
    PO = por[n]
    date = (datetime.now() + timedelta(days=7)).strftime("%Y%m%d")
    row = (invoicer[0],Part,Qty,Price,PO,date)
    csvRows.append(row)
    n = n+1

csvRows.sort()

outputfile = open('ConfirmPOLines.csv', 'a', newline='')
outputwriter = csv.writer(outputfile, dialect='excel')
for row in csvRows:
    outputwriter.writerow(row)
outputfile.close()

#shutil.move(file, "C:\\Users\\edwluk1\\Documents\\PDF\\Archive\\")
