
import os
from selenium import webdriver

import os, django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'education.settings')
django.setup()


from flashcards.models import *
from bs4 import BeautifulSoup

 
CONST_CATEGORY= "BUNIT14"
CONST_URL= 'https://www.sadlierconnect.com/anonymous/viewResource.html?resourceID=70349&programTOCId=2681&alias=vw&eventId=h97sikyHNRo98ys6&eventValidation=7be584aa4afeb792c45d804a104e5fee._.I3Z7e1ea_QI6U-6clmR9dvJ1EYR_X6XwW6jyx7U4aygmeMJd2mpp0-vAUQxEP4-0Mm6bbzkP8uVXOwa-NPZ31g~~'
driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get(CONST_URL)
driver.switch_to.frame('viewer')
html = driver.page_source

driver.close()



#soup = BeautifulSoup(open("cunit.html"), "html.parser")
soup = BeautifulSoup(html, "html.parser")

cards = soup.find_all('div', id=re.compile('^flipDiv_'))

print(len(cards))

for index in range(len(cards)) :
    print(f'flipDiv_{index}')
    text = soup.find('div', id=f'flipDiv_{index}').find('div', id=f'flipCardName_{index}').find('span')
    meaning = soup.find('div', id=f'flipDiv_{index}').find('div', id=f'flipCardImage_{index}').find('span')
    card = Card(category=CONST_CATEGORY, title=text.get_text(), meaning=meaning.get_text())
    card.save()
    print(f"text:{text.get_text()}")
    print(f"meaning:{meaning.get_text()}")
    