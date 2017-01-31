#turns sparex csv invoices into DHL friendly csv

#S0819 - invoice - part - desc - qty - total line value - GB - PO - SHIP - GBP

import os
import csv
from  tkinter import *
root = Tk()

os.chdir("G:\\Supply Chain\\CSV\\Shipment Uploads\\Working Files\\")

file=input('Enter filename for UK csv invoice:')

SHIP=input('Enter SHIP number:')

#root.filename =  filedialog.askopenfilename(initialdir = "G:\\Supply Chain\\CSV\\Shipment Uploads\\Working Files\\",title = "choose your file",filetypes = (("csv","*.csv"),("all files","*.*")))

csvRows = []
r = 0
#exampleFile = open(root.filename)
exampleFile = open(file)
exampleReader = csv.reader(exampleFile)
exampleData = list(exampleReader)
invoice = "invoice"
for row in exampleData:
    if exampleData[r][0] == 'INH':
        example = 0
    elif exampleData[r][0] == 'IDH':
        invoice = exampleData[r][5]
    elif exampleData[r][0] == 'IDD' and exampleData[r][1].isnumeric():
        Acc = 'S0819'
        part = exampleData[r][1]
        desc = exampleData[r][2]
        qty = exampleData[r][3]
        tlv = exampleData[r][6]
        gb = 'GB'
        po = exampleData[r][7]
        #SHIP = '1167' #change to user entered value
        gbp = 'GBP'
        drow = (Acc,invoice,part,desc,qty,tlv,gb,po,SHIP,gbp)
        print(drow)
        csvRows.append(drow)
    
    r=r+1

outputfile = open("G:\\Supply Chain\\Python Testing\\DHL.csv", 'w', newline='')
outputwriter = csv.writer(outputfile)
for row in csvRows:
    outputwriter.writerow(row)
outputfile.close()
root.withdraw()



