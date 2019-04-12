
# coding: utf-8

# In[1]:


#get_ipython().magic('matplotlib inline')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import xlsxwriter
import time
os.getcwd()


# In[2]:

'''
from IPython.core.display import HTML
css = open('style-table.css').read() + open('style-notebook.css').read()
HTML('<style>{}</style>'.format(css))
'''

# In[3]:


df = pd.read_excel('C:\\Users\\edwluk1\\Desktop\\Enn_ID.xls').fillna(value=0)

WOP = pd.read_excel('C:\\Users\\edwluk1\\Desktop\\WOP.xls').fillna(value=0)


# In[4]:


#Downsize unused columns 
cols = [2,4,5,6,7,9,11,12,13,14,19,20,21,22,23,24,25,26,27,28,29]
df.drop(df.columns[cols],axis=1,inplace=True)
df.drop([0],inplace=True)


# In[5]:


#Rename things 
df = df.rename(columns={
	'Item Number': 'part',
	'MRP Class': 'MRP',
    '12 Mth Sales Qty': '12ms',
    'Allocatable Qty': 'freeStock',
    'PO Qty (<=20)': 'open',
    'PO Qty (35, 40)': '40',
    'PO Qty (45)': '45'
	})

WOP = WOP.rename(columns={
	'Item Number': 'part',
	'Inbound Date': 'inbound',
        'PutAway Qty': 'putaway',
	'Unit Qty': 'qty',
	})


# In[6]:


WOP['putawaySum'] = WOP['putaway'].groupby(WOP['part']).transform('sum')

inboundP = dict(zip(
	WOP.part.values.tolist(),
	WOP.putawaySum.tolist(),
))


# In[7]:


df['putaway'] = df.part.map(inboundP).fillna(value=0)


# In[8]:


df.head()


# In[9]:


#Calculate the Percentages 
df['freeStock%'] = df['freeStock'].divide(df['12ms'])
df['putaway%'] = df['putaway'].divide(df['12ms'])
df['45%'] = df['45'].divide(df['12ms'])
df['40%'] = df['40'].divide(df['12ms'])
df['open%'] = df['open'].divide(df['12ms'])

df['total'] = df['freeStock%'] + df['putaway%'] + df['45%'] + df['40%'] + df['open%'] 


# In[10]:


#Create Empty Cells to fill with colour 
df=df.round(2)
df.head()

df.round(2)
df.head()
# In[11]:


os.chdir('//agsufs01/Supply/Replenishment/Transaction Data/Ennery/Ennery Stockout')


# In[12]:


timestr = time.strftime("%Y%m%d")

writer = pd.ExcelWriter('Ennery_Stockout_Review_%s.xlsx' % timestr, engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index=False)
workbook  = writer.book
worksheet = writer.sheets['Sheet1']


# In[13]:


#Colouring for freeStock 
format1 = workbook.add_format({'bg_color': '#FFC7CE'})
                               #'font_color': '#9C0006'})
    
format2 = workbook.add_format({'bg_color': '#35b019'})
                               #'font_color': '#9C0006'})

worksheet.conditional_format('K2:K7000', {'type': 'cell',
                                         'criteria': '<=',
                                         'value': 0.25,
                                         'format': format1})

worksheet.conditional_format('K2:K7000', {'type': 'cell',
                                         'criteria': '>',
                                         'value': 0.25,
                                         'format': format2})


# In[14]:


#Colouring for %putaway

format8 = workbook.add_format({'bg_color': '#f7ba0f'})

worksheet.conditional_format('L2:L7000', {'type': 'cell',
                                         'criteria': '>',
                                         'value': 0,
                                         'format': format8})


# In[15]:


#Colouring for %45

format3 = workbook.add_format({'bg_color': '#f7ba0f'})

worksheet.conditional_format('M2:M7000', {'type': 'cell',
                                         'criteria': '>',
                                         'value': 0,
                                         'format': format3})
                               


# In[16]:


#Colouring for %40

format4 = workbook.add_format({'bg_color': '#37d4d0'})

worksheet.conditional_format('N2:N7000', {'type': 'cell',
                                         'criteria': '>',
                                         'value': 0.1,
                                         'format': format4})
                           


# In[17]:


#Colouring for %open

format5 = workbook.add_format({'bg_color': '#ffcccc'})

worksheet.conditional_format('O2:O7000', {'type': 'cell',
                                         'criteria': '>',
                                         'value': 0.1,
                                         'format': format5})


# In[18]:


writer.save()

