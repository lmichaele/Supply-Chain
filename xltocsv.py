#! python3
# Runs over a folder, finds all the relevant files, updates the Customer Index spreadsheet

import openpyxl, csv

wb = openpyxl.load_workbook('C:\\Users\\edwluk5\\Desktop\\CIDupdate.xlsx')
sheet = wb.get_sheet_by_name('Information')3

Acc_no = sheet['I4'].value

Business_name = sheet['C4'].value

Business_address_line1 = sheet['C5'].value

Business_address_line2 = sheet['C6'].value

town = sheet['C6'].value

state = sheet['E6'].value

postcode = sheet['G6'].value

postal_address = sheet['C8'].value

general_phone = sheet['C9'].value

general_fax = sheet['G9'].value

business_email = sheet['C10'].value

website = sheet['G10'].value

last_visit = sheet['B11'].value

primary_contact = sheet['C14'].value

primary_contact_pos = sheet['G14'].value

primary_contact_phone = sheet['C15'].value

primary_contact_email = sheet['G15'].value

secondary_contact = sheet['C16'].value

secondary_contact_pos = sheet['G17'].value

secondary_contact_phone = sheet['C18'].value

secondary_contact_email = sheet['G18'].value

alt_contact = sheet['C20'].value

alt_contact_pos = sheet['G20'].value

alt_contact_phone = sheet['C21'].value

alt_contact_email = sheet['G21'].value

group_ind = sheet['C25'].value

no_of_branches = sheet['C26'].value

group_name = sheet['H25'].value

no_of_employees = sheet['H26'].value

workshop = sheet['C27'].value

no_of_mechanics = sheet['H27'].value

accessories = sheet['C28'].value

manufacturer = sheet['H28'].value

Update_by = sheet['B31'].value

Date = sheet['B32'].value

data_row = (Acc_no,Business_name,Business_address_line1,town,state,postcode,postal_address,general_phone,general_fax,business_email,website,last_visit,primary_contact,primary_contact_pos,primary_contact_phone,primary_contact_email)

outputfile = open('C:\\Users\\edwluk5\\Desktop\\Customer_Index.csv', 'a', newline='')
outputwriter = csv.writer(outputfile)
outputwriter.writerow(data_row)
outputfile.close()
