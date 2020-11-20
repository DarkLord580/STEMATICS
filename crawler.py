
import os
from selenium import webdriver

import os, django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'education.settings')
django.setup()


from flashcards.models import *
from bs4 import BeautifulSoup

 
CONST_CATEGORY= ""
CONST_URL= ''
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
    