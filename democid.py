import csv

#Parse update data, add to list

sauce = "C:\\Users\\edwluk5\Desktop\\demo.csv"
dest = "G:\\Supply Chain\\Customer Database\\Customer_Index_SPAU.csv"

csvrows = []
csvfile = open(sauce,'r')
reader = csv.reader(csvfile)
next(reader, None)
data = list(reader)

for row in data:
    csvrows.append(row)

print(csvrows)

destfile = open(dest,'a',newline='')
writer = csv.writer(destfile, dialect='excel')
for row in csvrows:
    writer.writerow(row)
destfile.close()

