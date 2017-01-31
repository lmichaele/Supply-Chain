import openpyxl, csv, os

EDR = openpyxl.load_workbook('G:\\Supply Chain\\Data\\SHIPMENTS\\Electronic Register - SGS.xlsx')

sheet = EDR.get_sheet_by_name('Register')

sheet.max_row

lship = sheet.cell(row=(sheet.max_row), column=2).value

print('Please enter your shipment number. The last used number was ' + str(lship)+'.')
SHIP = input()

