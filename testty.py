import csv

exampleFile = open('G:\\Supply Chain\\Python Testing\\SHIP1167.csv')
exampleReader = csv.reader(exampleFile)
exampleData = list(exampleReader)

r = 0

for row in exampleData:
    if exampleData[r][0] == 'IDH':
        Acc = 'S0819'
        part = [r][1]
        desc = [r][2]
        qty = [r][3]
        tlv = [r][6]
        gb = 'GB'
        po = [r][7]
        SHIP = '1167' #change to user entered value
        gbp = 'GBP'

        drow = (acc,invoice,part,desc,qty,tlv,gb,po,SHIP,gbp)

        print(drow)

r=r+1
