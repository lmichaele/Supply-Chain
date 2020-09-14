#!/usr/bin/env python

import tkinter as tk
import openpyxl, xlsxwriter, csv
from tkinter import filedialog
import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import time

pd.options.mode.chained_assignment = None  # default='warn'


tkroot = tk.Tk()
tkroot.withdraw()
file1 = filedialog.askopenfilename(title='Choose QV download')
afr = pd.read_excel(file1)
safr = pd.DataFrame() #service af df

vafr = pd.DataFrame() #VOR dataframe

safr = afr[['Item Number', 'Item Description', 'Demand', 'Current WAC','PO Qty 45']] #SER

vafr = afr[['Item Number', 'Item Description', 'Demand', 'Current WAC','PO Qty 45', 'CO VOR']] #VOR



spp = ['4392734M12',
       '0070004300000', '0974233330100', '0974240550500', 'ACW1586650',
       '0070065200000', '0070060300000',
       'Z099047000000', 'ACV0777320', 'ACV0256050', '4270520M11',
       '3789078M1', '4290866M3', 'V614901030', 'V615881216', 'V837067881', 'V837074972',
       'V837074813', 'V615892631', 'V615881418', 'V602084722',
       'ACW4034880', '4392674M16', '4390917M92', '002K120253100', 'Z416200010030', '0070389100000',
       '0974240550500', 'Z099053000000', '002K120920100', '4380771M18', 'H83597019027', 'ACW2775780', '3497161M91',
       'Z839201990010', '007F252891500', '4286889M97', '4393351M11', '525904D1', '4294998M91', '099K155900100',
       'Z735200012020', '099K155700000', '3930937M7', '4384530M12', '3384109M1', '3809693M91', '4379269M2',
       '4389564M94', '4389564M93', '4390170M1', '4391670M1', '3784628M93-4', '4385286M97', '3784591M2',
       '0963029300000', '3784628M94', '4281469M1', '4284843M95', 'BACW666829A00', '4384145M12', '0980026200000', '0980026200000',
       '007F253891500', 'VA342011', '002K115920100', 'ACX2498730', '3497244M91', '4366721M1', 'Z731200010020', 'Z738200990010',
       '009K155961100', '007H093960100', 'Z741200011013', '0070174200000', 'ACP0503890', 'ACP0503660', 'Z731200980020',
       'ACP0503720', 'ACP0503640', 'ACP0503650', 'ACP0503670', 'ACP0503690', 'ACP0503710', 'ACP0503740', 'ACP0503760',
       'ACP0503770', '0974259330600', '007F251891500', '0070036200000', '4315071M1', '4380811M17',
       '096K155800000', '7250104209', '7500640007', '3712626M1', '3931899M2', '4276429M91', '005A027800100', '093K120920100']


# In[5]:


safr['DLY qty'] = afr['CO DLY']
safr['STK qty'] = afr['CO STK']
safr['Other'] = afr['CO Other']
safr['Total'] = safr['DLY qty'] + safr['STK qty'] + safr['Other']


safr['Planned Date'] = pd.to_datetime(afr['Planned Date'], errors='coerce')

safr['Company'] = '501'
safr['Facility'] = 'AU1'
safr['Warehouse'] = 'AML'
safr['Supplier Code'] = '80050'
safr['Required Delivery date'] = (datetime.now() + timedelta(days=7)).strftime("%Y%m%d")
safr['Order Type'] = 'AIR'
safr['Suppress'] = afr['Item Number'].isin(spp)
safr['Kit'] = afr['Item Number'].str.startswith('349')


# In[6]:


vafr['Company'] = '501'
vafr['Facility'] = 'AU1'
vafr['Warehouse'] = 'AML'
vafr['Supplier Code'] = '80050'
vafr['Required Delivery date'] = (datetime.now() + timedelta(days=7)).strftime("%Y%m%d")
vafr['Order Type'] = 'VOR'

#iD = pd.read_excel('//eame.agcocorp.com/vinicius.guinossi/Supply/Python/Enn_ID.xls')
iD = pd.read_excel('C://Users//edwluk1//Desktop//Enn_ID.xls')
iD.rename(columns={'Item Number':'part'}, inplace=True)
iD.rename(columns={'MRP Class':'mrp'}, inplace=True)


# In[7]:


mrpC = dict(zip(
    iD.part.values.tolist(),
    iD.mrp.values.tolist(),
))

safr['MRP'] = afr['Item Number'].map(mrpC)
vafr['MRP'] = afr['Item Number'].map(mrpC)
#safr['Dealer Stk'] = (safr['Item Number'].map(partsL))
#vafr['Dealer Stk'] = (vafr['Item Number'].map(partsL))

eW = pd.read_excel('//eame.agcocorp.com/Luke.Edwards/Supply/Python/Enn_Weights.xlsx')

eW = eW.rename(columns={
    'Material Number (18)': 'part',
    'Net Weight (17.3)': 'weight',
    'Length (17.3)': 'lengths',
    'Width (17.3)': 'widths',
    'Height (17.3)': 'heights'
    })


# In[8]:


weights = dict(zip(
    eW.part.values.tolist(),
    eW.weight.values.tolist(),
))

lengths = dict(zip(
    eW.part.values.tolist(),
    eW.lengths.values.tolist(),
))

widths = dict(zip(
    eW.part.values.tolist(),
    eW.widths.values.tolist(),
))

heights = dict(zip(
    eW.part.values.tolist(),
    eW.heights.values.tolist(),
))


# In[9]:


safr['weight'] = safr['Item Number'].map(weights)
safr['L'] = safr['Item Number'].map(lengths)
safr['W'] = safr['Item Number'].map(widths)
safr['H'] = safr['Item Number'].map(heights)
safr['weight'] = safr['weight'].fillna(value='-')

vafr['weight'] = vafr['Item Number'].map(weights)
vafr['weight'] = vafr['weight'].fillna(value='-')


# In[10]:


#safr = safr[safr['DLY qty'] != 0]
vafr = vafr[vafr['CO VOR'] != 0]


# In[11]:


safr['Current WAC'] = safr['Current WAC'].round(2)
vafr['Current WAC'] = vafr['Current WAC'].round(2)

safr['MRP'] = safr['MRP'].fillna(value='<E')
safr.fillna(0, inplace=True)

vafr['MRP'] = vafr['MRP'].fillna(value='<E')
vafr.fillna(0, inplace=True)

safr = safr.sort_values(by=['MRP'], ascending=False)


# In[12]:


writer = pd.ExcelWriter('//eame.agcocorp.com/Luke.Edwards/Supply/Python/Airfreight Report.xlsx')
safr.to_excel(writer,'Service', index=False)
vafr.to_excel(writer,'VOR', index=False)

writer.save()

