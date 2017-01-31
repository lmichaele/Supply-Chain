import os
import csv
import datetime

os.chdir("G:\\Supply Chain\\CSV\\Shipment Uploads\\Working Files\\")

file=input('Enter filename for UK csv invoice:')

SHIP=file[0:8]

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
        SHIPinv = SHIP + "/" + invoice 
        part = exampleData[r][1]
        qty = exampleData[r][3]
        price = round(float(exampleData[r][6]) / float(exampleData[r][3]),2)
        po = exampleData[r][7]
        date = datetime.datetime.now().strftime("%Y%m%d")
        drow = (SHIPinv,part,qty,price,po,date)
        print(drow)
        csvRows.append(drow)
    r=r+1

os.chdir("G:\\Supply Chain\\CSV\\Shipment Uploads\\Ready to Load\\")

outputfile = open('%s' % "ok" + file, 'w', newline='')
outputwriter = csv.writer(outputfile)
for row in csvRows:
    outputwriter.writerow(row)
outputfile.close()
