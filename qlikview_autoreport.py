from selenium import webdriver
import pyautogui, time 
browser = webdriver.Firefox()

browser.get('http://edwluk1:Sicsempertyrannus99@qvserver/QvAJAXZfc/opendoc.htm?document=Parts%2FParts.qvw&host=QVS%40agmelap16')#open qv

pyautogui.press('left')#get rid of password dialogue

pyautogui.press('enter')

time.sleep(10)#wait for page to load, should be replaced with a wait function...

browser.find_element_by_xpath('/html/body/div[4]/div/ul/li[3]/a/span').click()#click on PCOM

time.sleep(10)

browser.find_element_by_xpath('/html/body/div[5]/div/div[187]/div[2]/div[1]/div').click()#click on excel export for CO mgmt summary

time.sleep(10)

pyautogui.press('left')#get rid of password dialogue

time.sleep(5)

pyautogui.press('space')

time.sleep(5)

pyautogui.press('down')

time.sleep(5)

pyautogui.press('enter')

#pyautogui.keyDown('ctrl'); pyautogui.press('w'); pyautogui.keyUp('ctrl')

time.sleep(5)

browser.find_element_by_xpath('/html/body/div[4]/div/ul/li[4]/a/span').click()#WOP

time.sleep(10)

browser.find_element_by_xpath('/html/body/div[5]/div/div[214]/div[3]/div/div[1]/div[5]/div/div[3]/div[2]/div/div[1]').click()#dropdown...

time.sleep(5)

browser.find_element_by_xpath('/html/body/div[9]/div/div/div[1]/div[3]/div[1]').click()#Planning Detail

time.sleep(5)

browser.find_element_by_xpath('/html/body/div[5]/div/div[163]/div[2]/div[1]/div').click()

time.sleep(5)

pyautogui.press('enter')

time.sleep(5)

pyautogui.keyDown('ctrl'); pyautogui.press('w'); pyautogui.keyUp('ctrl')

time.sleep(5)

browser.find_element_by_xpath('/html/body/div[5]/div/div[217]/div[3]/table/tbody/tr/td').click() #Outbound

time.sleep(5)

browser.find_element_by_xpath('/html/body/div[5]/div/div[163]/div[2]/div[1]/div').click() #excel 



