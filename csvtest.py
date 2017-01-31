import csv,os, locale

locale.setlocale(locale.LC_ALL, '')
path = ("G:\\Supply Chain\\Inventory Detail Reports\\Inventory_Details_Report.csv")
file = open(path, newline='',encoding="utf8")
reader = csv.reader(file)
header = next(reader)
header2 = next(reader)

WD = 260 #Working Dayss
LT = 110 #lead time
SS = 1.6 

data = []

for row in reader:
    #['Item Number', 'Item Description', 'Classification', 'MRP Class', 'Main Supplier', 'WH', 'Ops Location', 'COGS Last 12 Mths', '12 Mth Qty', 'SOH Value', 'Free Stock Value', 'Free Qty', 'PO Qty (<=20)', 'PO Qty (35/40)',
    # 'PO Qty (45)', 'Total PO Qty', 'DOs Out', 'DOs In', 'Optimum Qty', 'Potential Qty', 'Variance Qty', 'Risk', 'Optimum Turns', 'Actual Turns']
    WH = str(row[5])
    MRP = str(row[3])
    Part = str(row[0])
    Description = str(row[1])
    COGS = str(row[7])
    Twms = locale.atoi(row[8])
    Free = locale.atoi(row[11])
    line = WH,MRP,Part,Description,COGS,Twms,Free,(Twms)/WD*LT*SS

    if WH == 'SVI' and MRP == 'B:1-4':
        data.append(line)

out = open("G:\\Supply Chain\\Python Testing\\CSV\\new_po.csv", 'w', newline='', encoding="utf-8")
writer = csv.writer(out)

writer.writerow(['WH','MRP','Part','Description','COGS','Twms','Free','gen_po'])
for i in range(len(data) - 1):
    liney = data[i]
    writer.writerow(liney)
