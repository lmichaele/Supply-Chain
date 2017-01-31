#!python3
#this file opens a browser and downloads the inventory details report from Qlikview.
#it moves the old report but keeps the filename static so it can be referenced and refreshed in Excel

import time, datetime, os, shutil, pyautogui

from selenium import webdriver

from selenium.webdriver.support.ui import Select

browser = webdriver.Chrome()

browser.get('http://agmelap16/QvAJAXZfc/opendoc.htm?document=Sparex%2FSparex.qvw&host=QVS%40agmelap16')

time.sleep(10) # change to wait til load

browser.find_element_by_link_text('PIP').click()

time.sleep(5)

pyautogui.click(379, 284) # click inventory dropdown list

time.sleep(0.5)

browser.find_element_by_xpath("//*[@id='DS']/div/div/div[1]/div[2]").click()

time.sleep(5)

pyautogui.click(516, 283) # click WHS dropdown list

time.sleep(1)

pyautogui.click(480, 297)

time.sleep(5)

pyautogui.click(518, 440, button='right')

time.sleep(1)

pyautogui.click(551, 608) # clicks export

#browser.find_element_by_xpath("/html/body/ul/li[11]/a/span").click() #starts download

dte = datetime.datetime.now()
dt = dte.strftime('%y%m%d%H%M')
shutil.move('G:\\Supply Chain\\Inventory Detail Reports\\Inventory_Details_Report.csv', 'G:\\Supply Chain\\Inventory Detail Reports\\Inventory_Details_Report' + dt + '.csv') # moves old file to make way for new

os.chdir('C:\\Users\\edwluk5\\Downloads')

time.sleep(60) # wait for csv to download

fl = os.listdir(os.getcwd()) # these lines identify the new download by finding the newest file in the directory
fl = filter(lambda x: not os.path.isdir(x), fl)
newest = max(fl, key=lambda x: os.stat(x).st_mtime)
shutil.move(newest, 'G:\\Supply Chain\\Inventory Detail Reports\\Inventory_Details_Report.csv') # moves the new file

browser.close()
