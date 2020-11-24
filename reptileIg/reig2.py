import requests
import re
import json
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import time
import random

url = 'https://www.instagram.com/{get_who_pic}/'
uri = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    #     'cookie': 'mid=W4VyZwALAAHeINz8GOIBiG_jFK5l; mcd=3; csrftoken=KFLY0ovWwChYoayK3OBZLvSuD1MUL04e; ds_user_id=8492674110; sessionid=IGSCee8a4ca969a6825088e207468e4cd6a8ca3941c48d10d4ac59713f257114e74b%3Acwt7nSRdUWOh00B4kIEo4ZVb4ddaZDgs%3A%7B%22_auth_user_id%22%3A8492674110%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%228492674110%3Avsy7NZ3ZPcKWXfPz356F6eXuSUYAePW8%3Ae8135a385c423477f4cc8642107dec4ecf3211270bb63eec0a99da5b47d7a5b7%22%2C%22last_refreshed%22%3A1535472763.3352122307%7D; csrftoken=KFLY0ovWwChYoayK3OBZLvSuD1MUL04e; rur=FRC; urlgen="{\"103.102.7.202\": 57695}:1furLR:EZ6OcQaIegf5GSdIydkTdaml6QU"'
    'cookie': 'ig_did=9E2C00FC-0467-45E0-B026-020FBF18E1A8; csrftoken=OGhGBGq4Luch2PkcK4GdON878pHXNTV9; mid=X21VHQALAAFAllKyI0zA42WY2kQg;'
}


def get_who_html(who):
    try:
        # print(url)
        url_who = url.format(get_who_pic=who)
        # print(url_who)
        response = requests.get(url_who, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('请求错误状态码：', response.status_code)
            return response.status_code
    except Exception as e:
        print(e)
        return None


# html1 = get_who_html('yukakuramoti')


# print(html1)

def get_json(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print('请求网页json错误, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        time.sleep(60 + float(random.randint(1, 4000)) / 100)
        return get_json(url)


def get_urls(who):
    html = get_who_html(who)
    if html == 404:

        return 404

    urls = []
    url_video = []
    url_photo = []
    member_data = dict()
    user_id = re.findall('"profilePage_([0-9]+)"', html, re.S)[0]
    # print('user_id：' + user_id)
    # doc = pq(html)
    # items = doc('script[type="text/javascript"]').items()
    # print(items)

    soup = BeautifulSoup(html, 'html5lib')
    # print(soup)

    items = soup.find_all("script", type="text/javascript")
    # print(items)

    for item in items:
        # print(item.text.strip().startswith('window._sharedData'))
        if item.text.strip().startswith('window._sharedData'):
            js_data = json.loads(item.text[21:-1])
            edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"][
                'page_info']
            cursor = page_info['end_cursor']
            flag = page_info['has_next_page']
            for edge in edges:
                if edge['node']['display_url']:
                    display_url = edge['node']['display_url']
                    # print(display_url)
                    urls.append(display_url)
            # print(cursor, flag)
    while flag:
        url = uri.format(user_id=user_id, cursor=cursor)
        js_data = get_json(url)
        infos = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
        cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        # print(flag)
        for info in infos:
            if info['node']['is_video']:
                video_url = info['node']['video_url']
                if video_url:
                    # print(video_url)
                    urls.append(video_url)
                    url_video.append(video_url)

            else:
                if info['node']['display_url']:
                    display_url = info['node']['display_url']
                    # print(display_url)
                    urls.append(display_url)
                    url_photo.append(display_url)

        # print(cursor, flag)
        # time.sleep(4 + float(random.randint(1, 800))/200)    # if count > 2000, turn on
        member_data['photo'] = url_photo
        member_data['video'] = url_video
    return member_data


if __name__ == '__main__':
    # pyoapple
    # yukakuramoti
    print(get_urls('yukakuramoti'))
