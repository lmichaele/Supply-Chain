#create seafreight order
import os, csv, datetime

idr = ("G:\\Supply Chain\\Inventory Detail Reports\\Inventory_Details_Report.csv")

csvRows = []
r = 2

exampleFile = open(idr)
exampleReader = csv.reader(exampleFile)
exampleData = list(exampleReader)

for row in exampleData:
    if exampleData[r][4] == '1 - SPAREX UK':
        supplier = 1
    if exampleData[r][5] == 'SVI':
        state = 'SVI'
    if exampleData[r][3] == 'A:A-1':
        if float(exampleData[r][8].replace(',','') ) > 0:
            rqd = datetime.datetime.now().strftime("%Y%m%d")
            supplier = '1'
            state = 'SVI'
            OTP = 'SEA'
            DMT = 'SEA'
            part = exampleData[r][0]
            qty = float(exampleData[r][8].replace(',','')) / 267 * 100
            row = ('505','SP1',state,supplier,rqd,OTP,DMT,part,qty)
            print(row)
        csvRows.append(row)

    r=r+1

os.chdir("G:\\Supply Chain\\Python Testing\\")

outputfile = open('PO_test.csv', 'w', newline='')
outputwriter = csv.writer(outputfile)
for row in csvRows:
    outputwriter.writerow(row)
outputfile.close()
