from selenium import webdriver
from bs4 import BeautifulSoup
import pymysql as p
import requests
import json
import time

host = '127.0.0.1'
dbUser = 'root'
dbPasswd = '123456'
db = 'reptiledata'

ig_url_first = 'https://www.instagram.com/'

ig_url_middle = 'yukakuramoti'

ig_url_end = '/?hl=zh-tw'

custom_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'cookie': 'ig_did=9E2C00FC-0467-45E0-B026-020FBF18E1A8; csrftoken=OGhGBGq4Luch2PkcK4GdON878pHXNTV9; mid=X21VHQALAAFAllKyI0zA42WY2kQg; urlgen="{\"60.251.61.99\": 3462}:1kLiwf:jUvW3-f6WoQYgtx2k1VFqYeJHBw"'}

conn = p.connect(host, dbUser, dbPasswd, db)
cur = conn.cursor()


def get_urls(url):
    try:
        res = requests.get(ig_url_first, headers=custom_headers)
        if res.status_code == 200:
            return res.text
        else:
            print('請求錯誤狀態碼：', res.status_code)
    except Exception as e:
        print(e)
        return None


html = get_urls(ig_url_first)
print(html)


def get_ig_data(who):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        chrome = webdriver.Chrome(
                                  executable_path='D:/data/python/python_chrome_driver/chromedriver_win32/chromedriver')
        chrome.set_page_load_timeout(10)
        chrome.get(ig_url_first + ig_url_middle + ig_url_end)
        soup = BeautifulSoup(chrome.page_source, 'html5lib')
        titileName = soup.find('div', 'nZSzR').children.find('h2')
        print(titileName.text)
        ig_url = ig_url_first + who + ig_url_end
        # print(ig_url)
        gen_resp = requests.get(ig_url, headers=custom_headers)

        soup = BeautifulSoup(gen_resp.text, 'html5lib')
        # print(soup)
        titileName = soup.find('div', {'id': 'react-root'})
        print(titileName)

    except Exception as e:
        print(e)
    finally:
        # chrome.quit()
        cur.close()
        conn.close()


get_ig_data(ig_url_middle)
