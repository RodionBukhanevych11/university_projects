from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
from selenium import webdriver
import collections
import ssl

import selenium
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')


pages = set()
random.seed(datetime.datetime.now())
chrome_path = r"D:/repos/chromedriver.exe"
driver = webdriver.Chrome(chrome_path,options=options)


def getUsers(link):
    users=[]
    driver.get(link)

    while True:
        try:
            current=driver.current_url
            print(current)
            html = urlopen(current)
            bsObj = BeautifulSoup(html, 'lxml')
            for l in bsObj.findAll("a", href=re.compile("^(https://habr.com/ru/users/([^/?]+))")):
                if l.attrs['href'] is not None:
                    if l.attrs['href'] not in users:
                        users.append(l.attrs['href'])
                    else:  continue
            driver.find_element_by_id('next_page').click()
        except selenium.common.exceptions.NoSuchElementException:
            print("End of topic")
            break
    return users



def getExternalLinks(bsObj):
    externalLinks = []
    while True:
         try:
            for link in bsObj.findAll("a", href=re.compile("^(https://habr.com/ru/post/)")):
                if link.attrs['href'] is not None:
                    if link.attrs['href'] not in externalLinks:
                        if ('#habracut' in link.attrs['href']) or ('#comments' in link.attrs['href']):
                            continue
                        else:
                            externalLinks.append(link.attrs['href'])
            for link in bsObj.findAll("a", href=re.compile("^(https://habr.com/ru/company/([^/?]))")):
                if link.attrs['href'] is not None:
                    if link.attrs['href'] not in externalLinks:
                        if 'blog' in link.attrs['href']:
                            if ('#habracut' not in link.attrs['href']) and ('#comments' not in link.attrs['href']):
                                externalLinks.append(link.attrs['href'])
            driver.find_element_by_id('next_page').click()
         except selenium.common.exceptions.NoSuchElementException:
            print("End of topic")
            break
    return externalLinks


def extract_username(urls):
    names = collections.defaultdict(list)
    for link in urls:
        names[link].append(re.search(r'https://habr.com/ru/users/([^/?]+)', link).group(1))

    return names


def getAllExternalLinks(siteUrl):
    users_url = getUsers(siteUrl)
    i=0
    dict = extract_username(users_url)
    for user in dict.keys():
        user_html=urlopen(user+'posts/')
        bsObj2=BeautifulSoup(user_html,'lxml')
        externalLinks = getExternalLinks(bsObj2)
        for link in externalLinks:
                        html = urlopen(link)
                        bsObj = BeautifulSoup(html,'lxml')
                        driver.get(link)
                        data = driver.find_element_by_id("post-content-body")
                        title = driver.find_element_by_class_name("post__title-text")
                        try:
                            mark = driver.find_element_by_xpath("//span[@class='voting-wjt__counter  voting-wjt__counter_positive  js-score']")
                        except selenium.common.exceptions.NoSuchElementException:
                            print("negative mark")
                        try:
                            mark = driver.find_element_by_xpath("//span[@class='voting-wjt__counter   voting-wjt__counter_negative js-score']")
                        except selenium.common.exceptions.NoSuchElementException:
                            print("positive mark")
                        print(dict[user], title.text)
                        with open('D:/repos/TEXTS_ml/{}_Post_{}.txt'.format(dict[user], re.sub(r'\W+', ' ', title.text)), 'w', encoding='utf8') as output:
                            output.write(str(("Title " + title.text + "\nTEXT: " + data.text + "\n\nMARK: " + mark.text)))

                        i=i+1


if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    getAllExternalLinks("https://habr.com/ru/search/page9/?target_type=users&order_by=relevance&q=machine+learning&flow=")

