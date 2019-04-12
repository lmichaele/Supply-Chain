#Air Freight Report 2.0

#Splits the SER and VOR on different tabs

import tkinter as tk
import openpyxl, xlsxwriter, csv
from tkinter import filedialog
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None  # default='warn'

from datetime import timedelta, datetime

tkroot = tk.Tk()
tkroot.withdraw()
file1 = filedialog.askopenfilename(title='Choose QV download')
afr = pd.read_excel(file1)
safr = pd.DataFrame() #service af df

vafr = pd.DataFrame() #VOR dataframe

safr = afr[['Item Number', 'Item Description', 'Demand', 'Current WAC','PO Qty 45']] #SER

vafr = afr[['Item Number', 'Item Description', 'Demand', 'Current WAC','PO Qty 45', 'CO VOR']] #VOR


# !!!Parts to suppress from SERVICE AF due to weight size etc, review weekly

spp = ['4392734M12',
       '0070004300000', '0974233330100', '0974240550500', 'ACW1586650',
       '0070065200000', '0070060300000',
       'Z099047000000', 'ACV0777320', 'ACV0256050', '4270520M11',
       '3789078M1', '4290866M3', 'V614901030', 'V615881216', 'V837067881', 'V837074972',
       'V837074813', 'V615892631', 'V615881418', 'V602084722',
       'ACW4034880', '4392674M16', '4390917M92', '002K120253100', 'Z416200010030', '0070389100000',
       '0974240550500', 'Z099053000000', '002K120920100', '4380771M18']

# !!!END!!!

### SER ###

safr['SER qty'] = afr['CO DLY'] + afr['CO STK'] + afr['CO Other']

safr['Planned Date'] = pd.to_datetime(afr['Planned Date'], errors='coerce')

safr['Company'] = '501'
safr['Facility'] = 'AU1'
safr['Warehouse'] = 'AML'
safr['Supplier Code'] = '80050'
safr['Required Delivery date'] = (datetime.now() + timedelta(days=7)).strftime("%Y%m%d")
safr['Order Type'] = 'AIR'
safr['Suppress'] = afr['Item Number'].isin(spp)

### END SER ###

### VOR ###

vafr['Company'] = '501'
vafr['Facility'] = 'AU1'
vafr['Warehouse'] = 'AML'
vafr['Supplier Code'] = '80050'
vafr['Required Delivery date'] = (datetime.now() + timedelta(days=7)).strftime("%Y%m%d")
vafr['Order Type'] = 'VOR'

iD = pd.read_excel('C://Users//edwluk1//Desktop//Enn_ID.xls')
iD.rename(columns={'Item Number':'part'}, inplace=True)
iD.rename(columns={'MRP Class':'mrp'}, inplace=True)

mrpC = dict(zip(
    iD.part.values.tolist(),
    iD.mrp.values.tolist(),
))

safr['MRP'] = afr['Item Number'].map(mrpC)
vafr['MRP'] = afr['Item Number'].map(mrpC)

eW = pd.read_excel('//agsufs01/Supply/Python/Enn_Weights.xlsx')

weights = dict(zip(
    eW.part.values.tolist(),
    eW.weight.values.tolist(),
))

safr['weight'] = safr['Item Number'].map(weights)
safr['weight'] = safr['weight'].fillna(value='-')

vafr['weight'] = vafr['Item Number'].map(weights)
vafr['weight'] = vafr['weight'].fillna(value='-')

safr = safr[safr['SER qty'] != 0]
vafr = vafr[vafr['CO VOR'] != 0]

safr['MRP'] = safr['MRP'].fillna(value='<E')
safr.fillna(0, inplace=True)

vafr['MRP'] = vafr['MRP'].fillna(value='<E')
vafr.fillna(0, inplace=True)

safr = safr.sort_values(by=['MRP'], ascending=False)

writer = pd.ExcelWriter('Airfreight Report.xlsx')
safr.to_excel(writer,'Service', index=False)
vafr.to_excel(writer,'VOR', index=False)
writer.save()

