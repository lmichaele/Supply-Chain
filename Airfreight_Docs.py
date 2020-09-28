import xml.etree.ElementTree as ET
#import tkinter as tk
#from tkinter import filedialog
import re, csv, os, shutil, xlsxwriter
from datetime import timedelta, datetime
import pandas as pd
import win32com.client


outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)

#subject = mail.Subject
#attachment = mail.Attachments
file_home_path = '//eame.agcocorp.com/Luke.Edwards/Supply/Python/DHL_Airfreight/'

for message in inbox.Items:
    if message.UnRead == True:
        try:
            AWB = re.search(r"PRE_ALERT_(\d\D{3}\d{3})_AGCO", message.Subject).group(1)
            print(AWB) # Or whatever code you wish to execute.
            #attachment.SaveAsFile(os.path.join(file_home_path, AWB))
            Invoices = (re.findall(r"(A\d{7})", message.Body, flags=0))
            print(Invoices)
        except:
            pass
        try:
            AF_Folder = os.mkdir('//eame.agcocorp.com/Luke.Edwards/Supply/Python/DHL_Airfreight/' + AWB)
            for attachment in message.Attachments:
                print(attachment.Filename)
                #invoice_pdf = '{}.pdf'.format(AWB)
                #attachment.SaveAsFile(os.path.join(file_home_path, invoice_pdf))
                AF = ('//eame.agcocorp.com/Luke.Edwards/Supply/Python/DHL_Airfreight/' + AWB)
                attachment.SaveAsFile(AF + '{}.pdf')
                #print("pdf saved")
        except:
            pass
        


for message in inbox.Items:
  if message.UnRead == True:         
      try:
          Invoice = re.search(r"AGCO PARTS INVOICE (A\d{7}) 81411-002", message.Subject).group(1)
          print(Invoice)
          for attachment in message.Attachments:
              invoice_xml = '{}.xml'.format(Invoice)
              attachment.SaveAsFile(os.path.join(file_home_path, invoice_xml))
      except:
          pass


for filename in os.listdir(file_home_path):
    if filename.endswith(".xml"):
        file = (file_home_path + filename)
        tree = ET.parse(file)
        root = tree.getroot()
        xmlstr = ET.tostring(root, encoding='utf8', method='xml')       
        ln = re.findall(r'<LineNumber>(\d*)</LineNumber>', (str(xmlstr)))
        inv = re.findall(r'<InvoiceNumber>(........)', (str(xmlstr)))
        pnol = re.findall(r'<PartNumberOrdered>([^<]+)</PartNumberOrdered>', (str(xmlstr)))
        dfb = pd.DataFrame(dict(B=(pnol)))
        dfb.B = dfb.B.apply('="{}"'.format)
        pnsl = re.findall(r'<PartNumberSupplied>([^<]+)</PartNumberSupplied>', (str(xmlstr)))
        df = pd.DataFrame(dict(A=(pnsl)))
        df.A = df.A.apply('="{}"'.format)
        qtys = re.findall(r'<QuantitySent>(\d*)</QuantitySent>', (str(xmlstr)))
        price = re.findall(r'<UnitPrice>([^<]+)</UnitPrice>', (str(xmlstr)))
        orderref = re.findall(r'</OrderCategory><CustomerOrderRef>([^<]+)</CustomerOrderRef>', (str(xmlstr)))
        dateissue = re.findall(r'<DateOfIssue>(\d{8})</DateOfIssue>', (str(xmlstr)))
        partdiff = [i for i, j in zip(pnol, pnsl) if i != j]
        if not partdiff:
            print("All parts match original order.")
        else: print("Parts different from original PO (check validity in M3);"+(str(partdiff)))
        csvRows = []
        csvRows2 = []
        dcsvRows = []
        n = 0
        while n < len(ln): 
            partsupd = (str(pnsl[n])).replace(" ","")
            partsup = (df.A[n].replace(" ",""))
            qty = qtys[n]
            prc = price[n]
            po = orderref[n]
            doi = dateissue[0]
            partordd =  (str(pnol[n])).replace(" ","")

            if pnsl.count(pnsl[n]) > 1:
                Count = "TRUE"
            else:
                Count = "FALSE"
            if not po.isnumeric():
                print("Warning: Check Purchase Order Reference "+po)
            if pnsl[n] == pnol[n]:
                partord = ""
            else: 
                partord = (dfb.B[n].replace(" ",""))

            date = (datetime.now() + timedelta(days=7)).strftime("%Y%m%d")
            today = (datetime.now().strftime("%Y%m%d"))
            calc = (float(qty)) * (float(prc))
            row = ((', '.join(inv)),partsup,qty,prc,po,date,calc,Count,doi,partord)
            drow = ((', '.join(inv)),partsupd,qty,prc,po,date,calc,Count)
            if po.startswith('300'):
                afrow = (partsup, qty, po, today)
                csvRows2.append(afrow)
            csvRows.append(row)
            dcsvRows.append(drow)
            n = n+1
        csvRows.sort()

        newrows = []
        n=1
        k=2
        o=3
        newrows.append(csvRows[0])
        for row in csvRows:
            try:
                if csvRows[k][1]+csvRows[k][4] == csvRows[n][1]+csvRows[n][4]:
                    newrow = (csvRows[n][0],csvRows[n][1],int(csvRows[n][2])+int(csvRows[k][2]),csvRows[n][3],csvRows[n][4],csvRows[n][5]) #Add n+1 in to skip over the line
                    n=n+1
                    k=k+1
                else: newrow = (csvRows[n])
                newrows.append(newrow)
                n=n+1
                k=k+1
            except IndexError:
                continue

        outputfile = open('//eame.agcocorp.com/Luke.Edwards/Supply/Python/DHL_Airfreight/ConfirmPOLines_%s.csv' %filename[:-4], 'a', newline='')
        outputwriter = csv.writer(outputfile, dialect='excel')
        for row in csvRows:
            outputwriter.writerow(row)
        outputfile.close()

        outputfile2 = open('//eame.agcocorp.com/Luke.Edwards/Supply/Replenishment/AF Frequency Review/Ennery_AF_Frequency.csv', 'a', newline='')
        outputwriter2 = csv.writer(outputfile2, dialect='excel')
        for row in csvRows2:
            outputwriter2.writerow(row)
        outputfile2.close()
        
        r = 0
        c = 0

        inv1 = (', '.join(inv))

        outputfile = xlsxwriter.Workbook('//eame.agcocorp.com/Luke.Edwards/Supply/Python/Dissection_Invoice_%s.xlsx' % inv1)
        sheet = outputfile.add_worksheet('Dissection')

        for row in csvRows:
            sheet.write_row(r,c, row)
            r +=1

        outputfile.close()
        
        shutil.move(file,'//eame.agcocorp.com/Luke.Edwards/Supply/Python/Invoice Archives/')
    else:
        continue
    