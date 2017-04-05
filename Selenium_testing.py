from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait #these 3 extra selenium imports may be unneccesary
from selenium.webdriver.support import expected_conditions as EC#
from selenium.common.exceptions import TimeoutException#
import time, requests, bs4 
browser = webdriver.Firefox()
browser.get('https://agconet.agco.com.au/agconetStaffprod11/AGCOSystemlogin.cfm')

oldpart = 'G411971160021'
newpart = 'fgjfi'

username = browser.find_element_by_name("UserID")
password = browser.find_element_by_name("Password")

username.send_keys("edwluk1")
password.send_keys("P@ssw0rd99")

browser.find_element_by_xpath("//input[@value='Login']").click()

time.sleep(5)

browser.get('https://agconet.agco.com.au/agconetStaffprod11/PartDetails.cfm')

time.sleep(5)

partno = browser.find_element_by_name("TxtPartNum")
partno.send_keys(oldpart)

browser.find_element_by_name("Submit").click()

time.sleep(5)

oldstock = int(browser.find_element_by_xpath("/html/body/form/table[3]/tbody/tr[3]/td[9]/strong").text)

if oldstock > 0:
    suspncode = 'Suspn Code 11'
else:
    suspncode = 'Suspn Code 21'
print(suspncode)

browser.find_element_by_id("TxtPartNum").clear()

time.sleep(5)

partno = browser.find_element_by_name("TxtPartNum")
partno.send_keys(newpart)
browser.find_element_by_name("Submit").click()

time.sleep(5)

partstatus = browser.find_element_by_xpath("/html/body/form/table[2]/tbody/tr/td").text

if partstatus[0:10] == 'No Message':
    pcode = 'Y'
    print("New Part Exists")
else:
    pcode = 'N'
    print("New Part must be created in M3")


