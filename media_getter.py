import re
from get import get
import os
from random import random
from util import contains


_IMG_FILES = ['png', 'jpg', 'jpeg']
_VIDEO_FILES = ['gif', 'gifv', 'mp4', 'webm']


#a class that represents a piece of media
class _media():
    def __init__(self, path, title):
        self.path = path
        self.title = title

#determines if a link is one of the specified file_types
#if it is one of the types, the type is returned, otherwise None is returned
def _get_format(link, file_types):
    for t in file_types:
        if contains(r'\.' + t + r'$', link):
            return t
    return None

#determines if a file path is an image, for external use
def is_img(path):
    for t in _IMG_FILES:
        if contains(r'\.' + t + r'$', path):
            return True
    return False

#if the url points to any media then media is downloaded and returned, otherwise None is returned
#media is returned in a dictionary: {'data': get content, 'format': file extension}
def _get_media_data(url):
    if contains(r'^https?://(www\.)?gfycat\.com', url): #if gfycat gif, deals with http and https sites
        url = url.replace('gfycat.com', 'giant.gfycat.com').replace('www.', '') + '.mp4'
    if contains(r'^https?://i\.imgur\.com/.+?\.gifv', url): #if imgur gif
        url = url.replace('.gifv', '.mp4')
    format = _get_format(url, _IMG_FILES + _VIDEO_FILES)
    if format: #if the media is in one of the acceptable formats
        response = get(url)
        if response.status_code == 200: #make sure we got the content properly
            return {'data': response.content,
                    'format': format}
        else: #if there was a bad status code don't download the content
            print "GOT A WEIRD STATUS CODE: {0}".format(response.status_code)
    return None


#empties the folder at the specified file location
def _empty_folder(folder):
    for f in os.listdir(folder):
        os.remove(folder + '\\' + f)

#saves the image links to the specified folder
def save_media(posts, folder):
    _empty_folder(folder)
    all_media = []
    for p in posts:
        media = _get_media_data(p.url)
        if media is not None:
            print 'got ' + p.url
            with open('{0}\\{1}.{2}'.format(folder, random(), media['format']), 'wb') as f:
                f.write(media['data'])
                new_media = _media(os.path.abspath(f.name), p.title)
                all_media.append(new_media)
        else:
            print "couldn't get " + p.url
    return all_media
    


if __name__ == "__main__":
    save_media(['https://gfycat.com/CommonEagerAnemonecrab',
                'http://i.imgur.com/zQHVclH.gifv',
                'https://i.imgur.com/ANB928W.gifv',
                'https://i.imgur.com/rN5vkKj.jpg',
                'https://www.reddit.com/r/funny/comments/82pdwc/the_hand_of_meow/',
                'http://www.gfycat.com/ImpressionableWeeklyCero']
        ,'media')


'''
IMG_FILES = ['png', 'jpg', 'jpeg']
def is_img(link, response):
   return _is_format(link, response, IMG_FILES)

VIDEO_FILES = ['gif', 'gifv', 'mp4', 'webm']
def is_gif(link, response):
    return _is_format(link, response, VIDEO_FILES)


#saves the image links to the specified folder
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
'''
