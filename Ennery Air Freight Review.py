# Ennery Air Freight Review

# Get Inventory Details

# Get WOP

# AF Qty PO's Open 

# Ennery info from AGCO net  

# MRP Class, Part, Description, Supplier, Optimum, Potential, Free Qty, Inbound qty (WOP), Inbound Date (WOP), AF inbound (Open PO AF), (sums of sales etc),

# Import Id, WOP, Open PO, (\\agsufs01\Supply\Replenishment\Transaction Data\Ennery\Last12m\Ennery_Seasonality.xlsx) , 

import tkinter as tk
from tkinter import filedialog
import csv
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import datetime
from numpy.core.defchararray import add

tkroot = tk.Tk()
tkroot.withdraw()

idFile = filedialog.askopenfilename(title='Open Inventory Details')
ID = pd.read_excel(idFile)

wopFile = filedialog.askopenfilename(title='Open WOP')
WOP = pd.read_excel(wopFile)

afFile = filedialog.askopenfilename(title='Open AF')
AF = pd.read_excel(afFile)

DTF = pd.read_excel('//agsufs01/Supply/Replenishment/Transaction Data/Ennery/PCOMdf.xlsx')

ennSales = pd.read_excel('//agsufs01/Supply/Replenishment/Transaction Data/Ennery/Last12m/Ennery_Seasonality.xlsx')

afFreq = pd.read_csv('//agsufs01/Supply/Replenishment/AF Frequency Review/Ennery_AF_Frequency.csv')

df = pd.DataFrame()

ID = ID.rename(columns={
	'Item Number': 'part',
	'Item Description': 'desc',
	'MRP Class': 'MRP',
	})

#df.columns = (['MRP', 'Part', 'Description', 'Supplier', 'Optimum', 'Potential', 'Free Qty', 'Inbound Qty', 'Inbound Date', 'inbound AF', '3Q 17', '4Q 17', '1Q 18', '2Q 18', 'Spike', 'Short', 'af qty', 'Avg cost', 'Order Val'])
#df['Part'] = ID['part']
#df['MRP'] = ID['MRP']

cols = [2,5,6,7,9,11,12,13,14,16,17,18,19,20,21,22,25,26,27,28]
ID.drop(ID.columns[cols],axis=1,inplace=True)

WOP.sort_values(by=['Inbound Date'])

WOP = WOP.rename(columns={
	'Item Number': 'part',
	'Inbound Date': 'inbound',
        'PutAway Qty': 'putaway',
	'Unit Qty': 'qty',
	})

WOP['putawaySum'] = WOP['putaway'].groupby(WOP['part']).transform('sum')

WOP = WOP[~WOP.part.duplicated(keep='first')]


inboundQ = dict(zip(
	WOP.part.values.tolist(),
	WOP.qty.tolist(),
))

inboundD = dict(zip(
	WOP.part.values.tolist(),
	WOP.inbound.tolist(),
))

inboundP = dict(zip(
	WOP.part.values.tolist(),
	WOP.putawaySum.tolist(),
))

today = datetime.date.today()
margin = datetime.timedelta(days = 14)

ID['Inbound Date'] = ID['part'].map(inboundD)
ID['Inbound Qty'] = ID['part'].map(inboundQ)
ID['Putaway Qty'] = ID['part'].map(inboundP)

ID['Inbound Date'] = pd.to_datetime(ID['Inbound Date'], format="%d/%m/%Y")

conditions = [
     (ID['Inbound Date'] >= today + margin),
     (pd.isnull(ID['Inbound Date']))]

choices = ['1','1']

ID['2 weeks away'] = np.select(conditions, choices, default = '0')

#ID['2 weeks away'] = np.where((ID['Inbound Date'] >= today + margin) or pd.isnull(ID['Inbound Date']), '1', '0')
 
AF = AF.rename(columns={
	'Item Number': 'part',
	'Qty': 'qty',
	})

afQty = dict(zip(
	AF.part.values.tolist(),
	AF.qty.values.tolist(),
))

ID['Active AF qty'] = ID['part'].map(afQty)

#q417list = [10,11,12]
#q118list = [1,2,3]
q218list = [4,5,6]
q318list = [7,8,9]
q418list = [10,11,12]
q119list = [1,2,3]

#ennSales['q417'] =  ennSales[q417list].sum(axis=1)
#ennSales['q118'] =  ennSales[q118list].sum(axis=1)
ennSales['q218'] =  ennSales[q218list].sum(axis=1)
ennSales['q318'] =  ennSales[q318list].sum(axis=1)
ennSales['q418'] =  ennSales[q418list].sum(axis=1)
ennSales['q119'] =  ennSales[q119list].sum(axis=1)



q2 = dict(zip(
	ennSales.part.values.tolist(),
	ennSales.q218.values.tolist(),
))

q3 = dict(zip(
	ennSales.part.values.tolist(),
	ennSales.q318.values.tolist(),
))

q4 = dict(zip(
	ennSales.part.values.tolist(),
	ennSales.q418.values.tolist(),
))

q1 = dict(zip(
	ennSales.part.values.tolist(),
	ennSales.q119.values.tolist(),
))


#ID['Q417'] = ID['part'].map(q4)
#ID['Q118'] = ID['part'].map(q1)
ID['Q218'] = ID['part'].map(q2)
ID['Q318'] = ID['part'].map(q3)
ID['Q418'] = ID['part'].map(q4)
ID['Q119'] = ID['part'].map(q1)

"""
enn9 = ['Q417', 'Q118', 'Q218']
ID['spikeData'] = ID[enn9].sum(axis=1)
ID['spike'] = np.where(ID['spikeData'] < ID['Q318'], '1', '0') 
"""

enn9 = ['Q218', 'Q318', 'Q418']
ID['spikeData'] = ID[enn9].sum(axis=1)
ID['spike'] = np.where(ID['spikeData'] < ID['Q119'], '1', '0') 

ID.drop(ID.columns[18],axis=1,inplace=True)

ID['short'] = np.where(ID['Allocatable Qty'] < ID['Optim Qty'], '1', '0')

ID = ID.drop(ID.index[0])

ID['AF qty'] = ""

ID['Inbound Date'] = ID['Inbound Date'].dt.strftime('%d/%m/%Y')
ID['Inbound Date'] = np.where(ID['Inbound Date'] == 'NaT', 'open', ID['Inbound Date'])
ID['Avg Cost'] = np.round(ID['Avg Cost'], decimals=2)

ID['afFreq'] = ID['part'].map(afFreq['part'].value_counts())

dyf = DTF.pivot_table(index='part', columns='Fill', values='d2f', aggfunc='count', fill_value=0) 

ndf = dyf.div(dyf.sum(1), 0).mul(100).round(2).assign(Total=lambda dyf: dyf.sum(axis=1))

ndf = pd.DataFrame(ndf.to_records())

fillA = dict(zip(
	ndf.part.values.tolist(),
	ndf.A.values.tolist(),
))

fillB = dict(zip(
	ndf.part.values.tolist(),
	ndf.B.values.tolist(),
))

fillC = dict(zip(
	ndf.part.values.tolist(),
	ndf.C.values.tolist(),
))

ID['0 dF'] = ID['part'].map(fillA)
ID['1-5 dF'] = ID['part'].map(fillB)
ID['5+ dF'] = ID['part'].map(fillC)

writer = pd.ExcelWriter('Enn_Air_Freight_Review.xlsx')
ID.to_excel(writer,'Sheet1')
writer.save()

#WOP.loc[WOP['part'] == '3823621M96']
