import os
import pymysql
import pymysql.cursors
import re


def file_opt():
    for root, dirs, files in os.walk("D:\chaos"):
        for file in files:
            print(file)


def traverse(f):
    path_list = []
    fs = os.listdir(f)
    for f1 in fs:
        tmp_path = os.path.join(f, f1)
        if not os.path.isdir(tmp_path):
            path_list.append(tmp_path)
        else:
            path_list += traverse(tmp_path)
    return path_list


def link_mysql():
    connection = pymysql.connect(host='134.175.88.26',
                                 user='root',
                                 password='123456',
                                 db='fuskator',
                                 port=3306,
                                 charset='utf8')  # 注意是utf8不是utf-8
    try:
        with connection.cursor() as cursor:
            sql_1 = "insert into page_tag (link,tag) values ('%s', '%s' )" % ('https://fuskator.com/thumbs/fm0JArPDZCr/Teen-Shaved-Brunette-Babe-Izabel-A-from-Met-Art-Wearing-Purple-Lingerie-in-Bed.html', '1222222')
            cursor.execute(sql_1)
            # 提交到数据库执行
            connection.commit()
    finally:
        connection.close()


def str_del():
    text = 'kwL3MxFhHYL/Shaved-Teen-Blonde-Babe-Izabel-A-with-Meaty-Lips-Wearing-Yellow-Bikini-12.jpg'
    text_tpm1 = re.sub(r'-[0-9]*.jpg', '', text)
    text_tpm_list1 = text_tpm1.split("/")
    text_tpm_list1.reverse()
    text_tpm1 = "/".join(text_tpm_list1)
    text = text_tpm1 + "/" + text.split("/")[-1]
    print(text)


if __name__ == '__main__':
    str_del()


