import sys
import pymysql as p
import requests

# print(sys.path)
# if "\\Users\\LY\\PycharmProjects\\reptileData" not in sys.path:
#     sys.path.append('\\Users\\LY\\PycharmProjects\\reptileData\\reptileIg\\XX')

from reptileIg.reig2 import get_urls

host = '127.0.0.1'
dbUser = 'root'
dbPasswd = '123456'
db = 'reptiledata'


def get_data(who):
    try:
        conn = p.connect(host, dbUser, dbPasswd, db)
        cur = conn.cursor()
        # cur.execute("select * from myclub_ig")
        # print(cur.fetchall())

        url_list = get_urls(who)
        if url_list == 404:
            return 404

        phone_list = url_list.get('photo')
        for one_url in phone_list:
            sql = "INSERT INTO myclub_ig(img_name, img_url, remark) values('{}','{}','photo')".format(who, one_url)
            print(sql)
            cur.execute(sql)

        video_list = url_list.get('video')
        for one_url2 in video_list:
            sql = "INSERT INTO myclub_ig(img_name, img_url, remark) values('{}','{}','video')".format(who, one_url2)
            print(sql)
            cur.execute(sql)

        conn.commit()
    finally:
        conn.close()


def call_function():
    type_who = input("輸入你想要搜尋的IG 發表者: ")

    while get_data(type_who) == 404:
        type_who = input('您輸入的發布者並不存在或已失效，請重輸: ')
        get_data(type_who)


if __name__ == '__main__':
    call_function()
