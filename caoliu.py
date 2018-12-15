import os
import re
import shutil

import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


# 获取网页中图片的scr
def get_img_src(html):
    # 使用正则获取
    # srcs = re.findall(r"https://xoimg.club/u/\d+/\d+.jpg", html)
    # srcs = srcs+re.findall(r"https://www.touimg.com/u/\d+/\d+.jpg", html)

    # 使用元素选择器获取
    srcs = []
    page = BeautifulSoup(html, "lxml")
    imgs = page.select("input[type='image']")
    for imgEl in imgs:
        srcs.append(imgEl["data-src"])
    return srcs


# 下载图片
def download_img(img_src, pathfile):
    try:
        response = requests.get(img_src)
        response.encoding = 'utf-8'
        image = Image.open(BytesIO(response.content))
        imgname = img_src.split("/")[-1]
        if not os.path.exists(pathfile):
            os.makedirs(pathfile)
        image.save(pathfile+"/"+imgname)
    except IOError as e:
        print("IOError")
    except Exception as e:
        print("Exception")


# 下载列表中每个链接对应的页面图片
def download_page_line(line_url, pathfile):
    print("line_url is %s, pathfile is %s" % (line_url, pathfile))
    # pathfile = "D:/chaos/12"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.106 Safari/537.36'
    }
    # link = 'http://回家.tk/htm_data/8/1810/3314073.html'
    r = requests.get(line_url, headers=headers, timeout=10)
    r.encoding = 'utf-8'
    img_srcs = get_img_src(r.text)
    for img in img_srcs:
        download_img(img, pathfile)


# 获取标题和路径
def get_title_url(pageurl):
    titleurl_dict = dict()
    response = requests.get(pageurl)
    response.encoding = 'utf-8'
    page = BeautifulSoup(response.content, "lxml")
    trs = page.find_all('tr', class_='tr3 t_one tac')
    for tr in trs:
        if 'href' not in str(tr):
            continue
        # 获取到的其实是一个list
        a_el = tr.select("h3 a")
        if a_el is not None:
            a_el0 = a_el[0]
            a_url = a_el0["href"]
            a_title = a_el0.text
            if re.match(r'(.*)[\d+?P]', a_title):
                titleurl_dict[a_title] = a_url
    return titleurl_dict


# 删除数量小于20的文件夹
def rmfile(file_pre_path):
    if os.path.exists(file_pre_path):
        root_files_list = os.listdir(file_pre_path)
        for file in root_files_list:
            child_files_list = os.listdir(file_pre_path + "/" + file)
            if len(child_files_list) < 20:
                print("删除  " + file)
                # 递归删除
                #  os.remove(path)   #删除文件
                #  os.removedirs(path)   #删除空文件夹
                #
                # shutil.rmtree(path)    #递归删除文件夹
                shutil.rmtree(file_pre_path + "/" + file)


# 检查是否已存在该文件，如果存在，则从字典中删除
def distinct_dict(root_path, line_urls_dict):
    if os.path.exists(root_path):
        root_files_list = os.listdir(root_path)
        for file in root_files_list:
            if line_urls_dict[file] is not None:
                del line_urls_dict[file]


if __name__ == '__main__':
    file_pre_path = "D:/chaos/12/"
    page_pre_path = "http://回家.tk/"
    pageurl = "http://xn--zbsq6i.tk/thread0806.php?fid=8&search=&page=2"
    # 获取列表页面中各项的url和名称
    line_urls_dict = get_title_url(pageurl)
    distinct_dict(file_pre_path, line_urls_dict)
    print(line_urls_dict)
    # for k in line_urls_dict:
    #     download_page_line(page_pre_path+line_urls_dict[k], file_pre_path+k)
    # 删除数量小于20的文件夹
    rmfile(file_pre_path)

