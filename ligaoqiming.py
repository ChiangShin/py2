import os
import re
import shutil

import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


def get_title_and_url(root_url):
    titleurl_dict = dict()
    response = requests.get(root_url)
    response.encoding = 'utf-8'
    page = BeautifulSoup(response.content, "lxml")
    print(page)
    a_ele = page.find_all('li a')
    for a in a_ele:
        a0 = a[0]
        a_text = a0.text
        a_url = a0["href"]
        titleurl_dict[a_text] = a_url
    return titleurl_dict


if __name__ == '__main__':
     titleurl_dict = get_title_and_url("https://www.piaotian.com/html/1/1657/")
     print(titleurl_dict)