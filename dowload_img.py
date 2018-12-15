import math
import os
import random
import re
import requests
import time
import multiprocessing
from PIL import Image
from io import BytesIO


def read_file(path, file_name):
    # 待下载的图片
    f = open(path+file_name, mode="r")
    srcs = set(f.readlines())
    print("已保存的图片链接数："+str(len(srcs)))
    # 获取已保存的图片的名称
    saved_img_names = traverse(path)
    for i in range(len(saved_img_names)):
        saved_img_names[i] = saved_img_names[i].replace(path, '').replace("\\", '/')

    print("已保存的图片数set："+str(len(saved_img_names)))

    # 保存未下载的
    need_dowload_img_srcs = []
    for src in srcs:
        src_tmp = re.sub(r'.*large/', '', src).replace("\n", "")
        text_tpm1 = re.sub(r'-[0-9]*.jpg', '', src_tmp)
        text_tpm_list1 = text_tpm1.split("/")
        text_tpm_list1.reverse()
        text_tpm1 = "/".join(text_tpm_list1)
        text = text_tpm1 + "/" + src_tmp.split("/")[-1]
        if text not in saved_img_names:
           need_dowload_img_srcs.append(src)

    print("需要下载的数量need_dowload_img_srcs：" + str(len(need_dowload_img_srcs)))

    # 进程数
    jc_num = 10
    if len(need_dowload_img_srcs) > jc_num:
        # 每个进程分配的链接数量
        jc_size = math.ceil(len(need_dowload_img_srcs)/jc_num)
        res = partition(need_dowload_img_srcs, jc_size)
        for i in range(jc_num):
            multiprocessing.Process(target=dowload_task, args=(res[i], path,)).start()
    else:
        dowload_task(need_dowload_img_srcs, path)


def dowload_task(src_list, path):
    for src in src_list:
        src_tmp = re.sub(r'.*large/', '', src).replace("\n", "")
        text_tpm1 = re.sub(r'-[0-9]*.jpg', '', src_tmp)
        text_tpm_list1 = text_tpm1.split("/")
        text_tpm_list1.reverse()
        text_tpm1 = "/".join(text_tpm_list1)
        text = text_tpm1 + "/" + src_tmp.split("/")[-1]
        dir_name = path + text
        download_img(src, dir_name)


# 下载图片
def download_img(img_src, pathfile):
    try:
        sleeptime = random.randrange(0, 200)
        time.sleep(sleeptime/100)
        # print("img_src:"+img_src+"   pathfile:"+pathfile)
        response = requests.get(img_src)
        response.encoding = 'utf-8'
        image = Image.open(BytesIO(response.content))
        imgname = img_src.split("/")[-1]
        if not os.path.exists(pathfile):
            os.makedirs(pathfile)
        image.save(pathfile+"/"+imgname)
        print("下载成功：" + img_src)
    except IOError as e:
        print("IOError，下载失败："+img_src)
    except Exception as e:
        print("Exception")


# 获取文件夹下所有文件的全路径
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


def partition(ls, size):
    """
    Returns a new list with elements
    of which is a list of certain size.

        >>> partition([1, 2, 3, 4], 3)
        [[1, 2, 3], [4]]
    """
    return [ls[i:i+size] for i in range(0, len(ls), size)]


if __name__ == '__main__':
    read_file("D://chaos//", "Alessa_Z.txt")

