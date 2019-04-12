# have invoices ready

# load dhl paperwork

# get invoices from dhl paperwork

# process accordingly

# check value against correct total

#(process either xml or pdf)

#(must detect exchange surcharge)

from tabula import wrapper

import pandas as pd
import numpy as np 

from datetime import timedelta, datetime

import tkinter as tk
from tkinter import filedialog

import re, shutil, PyPDF2, os, glob

tkroot = tk.Tk()
tkroot.withdraw()
file = filedialog.askopenfilename()

pdfFileObj = open(file, 'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pageObj = pdfReader.getPage(0)
pageStr = pageObj.extractText()

invr = re.compile(r'(A0\d{6})')
Inv = invr.findall(pageStr)

directory = "//agsufs01/Supply/Ennery Invoices/"

file1 = "//agsufs01/Supply/Ennery_Invoices/" + Inv[0] + "INVOICE_DETAIL.PDF"

df = wrapper.read_pdf(file1, pages='all')

doi = re.compile(r'(\d\d/\d\d/\d\d)')
Dateoi = doi.findall(str(df['Unnamed: 2'].str.extract(r'(\d\d/\d\d/\d\d)')))


df = df.rename(columns={
    'AGCO International GmbH': 'data', 
    'Unnamed: 1': 'data1',
    'Unnamed: 2': 'data2',
})

#create empty df for dissection
#write individual lines to new df

invr = re.compile(r'(A0\d{6})')
Invoice = invr.findall(str(df['data'].str.extract(r'(A0\d{6})\s')))

df['mask'] = df['data'].str.contains('[DFGVWXYE]\d{7}\s')
df = (df[df['mask'] == True]).drop('mask', axis = 1)

# Purchase Orders to charge out

cpos = []

df['connection'] = Invoice[0]
df['part'] = df['data'].str.extract(r'[DFGVWXYE]\d{7}\s(.*)\s')
df['qty'] = df['data2'].str.extract(r'(\d*)\s') 
df['price'] = df['data2'].str.extract(r'\d*\s*\d*\s*(.*)\s') 
df['po'] = df['data'].str.extract(r'[DFGVWXYE]\d{7}\s*.*\s(.*)') 
df['date'] = (datetime.now() + timedelta(days=7)).strftime("%Y%m%d")
df['total'] = df['data2'].str.extract(r'\d*\s*\d*\s*.*\s(.*)') 
df['duplicate'] = df.duplicated(subset=['part', 'po'], keep=False)
df['chargeOut'] = df['po'].isin(cpos)
df['dateofissue'] = Dateoi[0]

af = pd.DataFrame()
af['part'] = df['data'].str.extract(r'[DFGVWXYE]\d{7}\s(.*)\s')
af['qty'] = df['data2'].str.extract(r'(\d*)\s') 
af['po'] = df['data'].str.extract(r'[DFGVWXYE]\d{7}\s*.*\s(.*)') 
af['date'] = (datetime.now())

df = df.drop(['data', 'data1', 'data2'], axis=1)

df.part = df.part.str.strip()
df.part = df.part.str.replace(" ", "")
df.part = df.part.apply('="{}"'.format)

df.to_csv('ConfirmPOLines.csv', mode='a', encoding='utf-8', index=False, header=False)

df.to_csv('Dissection_Invoice.csv', mode='a', encoding='utf-8', index=False, header=False)

with open('//agsufs01/Supply/Replenishment/AF Frequency Review/Ennery_AF_Frequency.csv', 'a') as f:
    af.to_csv(f, index=False, header=False, )


shutil.move(file,'//agsufs01/Supply/Python/Invoice Archives/')




