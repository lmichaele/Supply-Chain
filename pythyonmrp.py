import unicodecsv as csv
import sys

lead_time = 90

working_days = 260

with open('C:\\Users\\edwluk5\\Desktop\\inventorydetails.csv', 'rb') as f:
    reader = csv.reader(f)
    data = [next(reader)]  # title rows
    for row in reader:
        if row[8] > '0':
            if row[2] == 'A':
                ssf = 1.9
            elif row[2] == 'B':
                ssf = 1.5
            elif row[2] == 'C':
                ssf = 1
            elif row[2] == 'D':
                ssf = 0.8
            elif row[2] == 'E':
                ssf = 0
            data.append(row + [float(row[8]) / working_days * lead_time * ssf])

with open('Python_MRP.csv', 'wb') as nf:
    writer = csv.writer(nf)
    writer.writerows(data)
