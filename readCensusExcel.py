#! python 3
# readCensusExcel.py  -  Tabulates popuylation and number of census tracts
# for each county.

import openpyxl, pprint
print('Opening workbook...')
wb = openpyxl.load_workbook('censuspopdata.xlsx')
sheet = wb.get_sheet_by_name('Population by Census Tract')
countData = {}

    # TODO: Fill in countyData with each county's population and tracts.
    
print('Reading rows...')
for row in range(2, sheet.max_row + 1):
        # Each row in the speadsheet has data for one census tract
        state  = sheet['B' + str(row)].value
        county = sheet['C' + str(row)].value
        pop    = sheet['D' + str(row)].value

    # TODO: Open a new text file and write the contents of countyData to it.

