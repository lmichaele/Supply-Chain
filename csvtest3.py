import csv

with open('G:\\Supply Chain\\Python Testing\\testcsv.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if int(row['COGS 12m']) > 0 and row['warehouse'] == 'SVI':
            print(row['part'], row['supplier'], row['qty'])
