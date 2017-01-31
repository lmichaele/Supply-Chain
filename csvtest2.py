import csv

idrfile = open('G:\\Supply Chain\\Inventory Detail Reports\\Inventory_Details_Report.csv')
idrreader = csv.DictReader(idrfile)
for row in idrreader:
        if idrreader.line_num == 2 and row['warehouse'] == 'SVI':
                print("okay")
