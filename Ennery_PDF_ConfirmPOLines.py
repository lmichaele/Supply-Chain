from tabula import wrapper

import pandas as pd
import numpy as np 

from datetime import timedelta, datetime

import tkinter as tk
from tkinter import filedialog

import re, shutil, csv

tkroot = tk.Tk()
tkroot.withdraw()
file = filedialog.askopenfilename()

df = wrapper.read_pdf(file, pages='all')

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

cpos = ['3006869', '3006870', '3006875', '3006883', '3006968', '3006975',
        '3007071WGS', '3007111', '4009494', '3007134', '4009515', '3007166',
        '4009529', '4009530', '3007023', '3007340']

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
    af.to_csv(f, header=False, index=False)


shutil.move(file,'//agsufs01/Supply/Python/Invoice Archives/')
