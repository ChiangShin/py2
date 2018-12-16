import pymysql
import pymysql.cursors
from urllib.request import urlopen
import dowload_img
import re


import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.106 Safari/537.36'
    }


def get_all_page_url(root_path, page_index, key_word):
    try:
        html = urlopen("https://fuskator.com/page/"+str(page_index)+"/"+key_word+"/quality/").read().decode("utf-8")
        url_list = re.findall(r'/thumbs/.*html', html)
        # 获取所有图片的链接
        tup1 = []
        for url in url_list:
            tup1 += get_page_img_src("https://fuskator.com"+url)
        f = open(root_path+key_word+".txt", mode="a+")

        for src in tup1:
            f.write(src)
            f.write("\n")
        f.close()
    except IOError as e:
        print("IOError")
    except Exception as e:
        print(e)


def get_page_img_src(page_url):
    # html = urlopen(page_url).read().decode("utf-8")
    # html = re.sub(r'small', 'large', html)
    # return re.findall(r'/large/.*-[0-9]+.jpg', html)

    r = requests.get(page_url, headers=headers, timeout=10)
    r.encoding = 'utf-8'

    srcs = []
    page = BeautifulSoup(r.text, "lxml")
    # tag
    tags = page.select("#spanTags")[0].text
    connection = pymysql.connect(host='134.175.88.26',
                                 user='root',
                                 password='123456',
                                 db='fuskator',
                                 port=3306,
                                 charset='utf8')  # 注意是utf8不是utf-8
    try:
        with connection.cursor() as cursor:
            sql_1 = "insert into page_tag (link,tag) values ('%s', '%s' )" % (page_url, tags)
            cursor.execute(sql_1)
            # 提交到数据库执行
            connection.commit()
    finally:
        connection.close()

    # 图片链接
    imgs = page.select("img.pic_pad")
    for imgEl in imgs:
        src = "https:"+imgEl["src"]
        src = re.sub(r'/small/', '/large/', src)
        srcs.append(src)
    return srcs


if __name__ == '__main__':
    key_word = 'Emily'
    root_path = 'D://chaos//'
    # for page_index in range(1, 6):
    #     get_all_page_url(root_path, page_index, key_word)
    dowload_img.read_file(root_path, key_word+".txt")


