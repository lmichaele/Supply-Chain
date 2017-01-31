import csv

path = ("/Users/lmichaele/Documents/inventory_details_copy.csv")
file = open(path, newline='', encoding="utf8")
reader = csv.reader(file)

header = next(reader)

WD = 260 #Working Days
LT = 100 #lead time

data = []
for row in reader:
    #['Item Number', 'Item Description', 'Classification', 'MRP Class', 'Main Supplier', 'WH', 'Ops Location', 'COGS Last 12 Mths', '12 Mth Qty', 'SOH Value', 'Free Stock Value', 'Free Qty', 'PO Qty (<=20)', 'PO Qty (35/40)',
    # 'PO Qty (45)', 'Total PO Qty', 'DOs Out', 'DOs In', 'Optimum Qty', 'Potential Qty', 'Variance Qty', 'Risk', 'Optimum Turns', 'Actual Turns']
    WH = str(row[5])
    MRP = str(row[3])
    Part = str(row[0])
    Description = str(row[1])
    COGS = float(row[7])
    Twms = float(row[8])

    Free = int(row[11])
    line = WH,MRP,Part,Description,COGS,Twms,Free,((Twms)/WD*LT)

    if WH == 'SVI' and MRP == 'B:1-4':
        data.append(line)

out = open('new_po.csv', 'w', encoding="utf-8")
writer = csv.writer(out)
#writer.writerow(["WH","Part","Description","MRP","Qty"])

for i in range(len(data) - 1):
    liney = data[i]
    writer.writerow(liney)
