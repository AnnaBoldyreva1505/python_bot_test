# Соберем информацию с сайта https://live.skillbox.ru/playlists/code/python/
# Библиотека OpenPyXL позволяет читать и записывать таблицы Excel

import requests
from openpyxl import Workbook
from bs4 import BeautifulSoup

web_page = requests.get('https://live.skillbox.ru/playlists/code/python/')
soup = BeautifulSoup(web_page.text, 'html.parser')

work_book = Workbook()
work_sheet = work_book.active

items = soup.find_all(class_='playlist-inner__item')

for elem in items:
    title_elem = elem.find(class_='playlist-inner-card__title t t--3')
    if title_elem:
        title = title_elem.text
    else:
        title = 'Title not found'

    relative_url = elem.find(class_='playlist-inner-card__link')
    if relative_url:
        relative_url = relative_url.attrs.get('href', '')
    else:
        relative_url = ''

    timing_elem = elem.find(class_='playlist-inner-card__small-info')
    if timing_elem:
        timing = timing_elem.text.strip().split(',')[-1].strip()
    else:
        timing = 'Timing not found'

    url = 'https://live.skillbox.ru' + relative_url
    row = [title, url, timing]
    print(row)
    work_sheet.append(row)

work_book.save('Вебинары про Python от Skillbox.xlsx')
