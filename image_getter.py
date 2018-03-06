import re
from get import get
import os
from random import random

def _is_format(link, response, file_types):
    for t in file_types:
        if len(re.findall(r'\.' + t + r'$', link)) != 0:
            return True
    #add more tests here
        

IMG_FILES = ['png', 'jpg', 'jpeg']
def is_img(link, response):
   return  _is_format(link, response, IMG_FILES)

VIDEO_FILES = ['gif', 'gifv', 'mp4']
def is_gif(link, response):
    return _is_format(link, response, VIDEO_FILES)


def _empty_folder(folder):
    for f in os.listdir(folder):
        os.remove(folder + '\\' + f)

def save_imgs(links, folder):
    _empty_folder(folder)
    downloaded = [(l, get(l)) for l in links]
    image_data = []
    for d in downloaded:
        if is_img(*d):
            image_data.append(d[1].content)
    img_paths = []
    for i in image_data:
        with open('images\\' + str(random()) + '.png', 'wb') as f:
            f.write(i)
            img_paths.append(os.path.abspath(f.name))
    return img_paths
    

