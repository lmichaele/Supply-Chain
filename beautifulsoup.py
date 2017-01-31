from bs4 import BeautifulSoup
import urllib.request

url="http://agmelap16/QvAJAXZfc/opendoc.htm?document=Sparex%2FSparex.qvw&host=QVS%40agmelap16"

page = urllib.request.urlopen(url)

soup = BeautifulSoup(page.read())

print(soup)
