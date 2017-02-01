import openpyxl, csv, os, time, glob, shutil, datetime

print ('Before starting, make sure all csv invoices are saved in Supply Chain > CSV > New Shipment.')

EDR = openpyxl.load_workbook('G:\\Supply Chain\\Data\\SHIPMENTS\\Electronic Register - SGS.xlsx')

sheet = EDR.get_sheet_by_name('Register')

sheet.max_row

lship = sheet.cell(row=(sheet.max_row), column=2).value

while True:
    try:
        SHIP = int(input("Please enter a shipment number. The last used number was " + str(lship)+".")) 
    except ValueError:
        print('Try again - make sure you have chosen a four digit number, that is bigger than ' + str(lship) +'.')
    else:
        break #TO DO - Make more rules, like correct number chosen etc 
print("Thanks. Creating folders and doing stuff...")

#add number to ER


directory = "G:\\Supply Chain\\Ship Files\\SHIP" + str(SHIP) + "\\"

if not os.path.exists(directory): #creates new ship folder
    os.makedirs(directory)

print("G:\\Supply Chain\\Ship Files\\SHIP" + str(SHIP) + "\\ has been created to store all documents relating to shipment")

time.sleep(4)

print("Now converting CSV files...")

os.chdir("G:\\Supply Chain\\CSV\Shipment Uploads\\New Shipment\\") 
read_files = glob.glob("*.csv")
with open("invoice.csv", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())
			
shutil.move("invoice.csv",(directory)+"SHIP"+str(SHIP)+".csv")

time.sleep(2)

#delfiles = glob.glob("*.csv") 
#for d in delfiles:
 #   os.remove(d)

print("Master invoice created. Now creating ConfirmPOLines...")

os.chdir(directory)

file = "SHIP"+str(SHIP)+".csv"

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
        SHIPinv = "SHIP"+str(SHIP) + "/" + invoice 
        part = exampleData[r][1]
        qty = exampleData[r][3]
        try:
            price = round(float(exampleData[r][6]) // float(exampleData[r][3]),2)
        except ZeroDivisionError:
            price = 0
        po = exampleData[r][7]
        date = datetime.datetime.now().strftime("%Y%m%d")
        drow = (SHIPinv,part,qty,price,po,date)
        print(drow)
        csvRows.append(drow)
    r=r+1

os.chdir("G:\\Supply Chain\\CSV\\Shipment Uploads\\Ready to Load\\")

outputfile = open('ConfirmPOLines.csv', 'w', newline='')
outputwriter = csv.writer(outputfile)
for row in csvRows:
    outputwriter.writerow(row)
outputfile.close()

time.sleep(5)

print("ConfirmPOLines created in Supply Chain > CSV > Shipment Uploads > Ready to Load")

time.sleep(3)

os.chdir(directory)

while True:
    try:
        DMT = str(input('Is this shipment Airfreight or Seafreight? (Enter A or S)'))
    except:
        print("Not a valid option. Try again")
    if DMT == 'A':
        print("Airfreight confirmed. Creating CSV invoice for DHL.")
        time.sleep(5)
        csvRows = []
        r = 0
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
                gbp = 'GBP'
                drow = (Acc,invoice,part,desc,qty,tlv,gb,po,SHIP,gbp)
                print(drow)
                csvRows.append(drow)
    
            r=r+1

        os.chdir("G:\\Supply Chain\\CSV\\Files for Freight Forwarders\\")

        outputfile = open('SHIP'+str(SHIP)+'_DHL.csv', 'w', newline='') #TODO create new and unused doc... 
        outputwriter = csv.writer(outputfile)
        for row in csvRows:
            outputwriter.writerow(row)
        outputfile.close()
        #root.withdraw()
        print('DHL invoice created in Supply Chain > CSV > Files for Freight Forwarders.')

        
    elif DMT == 'S':
        print('Seafreight confirmed.') #TODO create invoices for JAS
    else:
        print("Not a valid option. Please try again")

#TODO add to ER

        

