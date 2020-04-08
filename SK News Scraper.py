import requests
from bs4 import BeautifulSoup
import time
from urllib.request import urlopen
import re
import os
import urllib.request as req

total_page_number_to_crawl = 7 #number of pages you want to scrape
target_url = """https://www.sktelecom.com/en/press/press.do?page.page="""


file_path = "C:\\Users\\charl\\Desktop\\SK Pachong\\" + "urls.txt" #feel free to change the path name here

#Scrape down all the urls

for page in range(total_page_number_to_crawl):
    #print('Crawl Page: %d/%d' % (page+1, total_page_number_to_crawl))
    url = target_url + str((page + 1))
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    for ul in soup.find_all('ul'):
        for li in ul.find_all('li'):
            for a in li.find_all('a'):
                a_href = a.get('href')
                href_number_raw = re.findall(r"\d+\.?\d*", a_href)
                for number in href_number_raw:
                    print('https://www.sktelecom.com/en/press/press_detail.do?page.page=' + str(page + 1) + '&idx=' + number, file = open(file_path, "a", encoding='utf-8'))
    time.sleep(1)


#Download the articles

with open(file_path) as f:
    content = f.readlines()

for url in content:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find('p', attrs = {"class": "title"}).get_text() #Downloads the titles
    content = soup.find('div', attrs = {"class": "board-detail-body"}).get_text() #Downloads the contents
    total = url + '\xa0\n' + title + '\xa0\n' + content
    path = "C:\\Users\\charl\\Desktop\\SK Pachong\\" + title + ".txt"
    print(total, file=open(path, "a", encoding='utf-8'))


#Download the images

for url in content:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find('p', attrs = {"class": "title"}).get_text()
    for p in soup.find_all('p'):
        for img in p.find_all('img'):
            img_src = img.get('src')
            req.urlretrieve(img_src, title + ".jpg")
