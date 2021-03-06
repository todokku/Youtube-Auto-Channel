import requests
import re
from random import random
import os
from get import get as good_get
from util import find_first
import time


def get(url):
    return good_get(url).content


class corrupt_song_link_exception(Exception):
    pass

def corrupt_if_none(func):
    def true_func(self):
        val = func(self)
        if val is None:
            raise corrupt_song_link_exception("Broken link!")
        return val
    return true_func


class song:
    
    def __init__(self, url):
        self._url = url
        self._track_page = get(url)
        self._data = get(self._download_link())
        self._artist, self._name = self._get_info()
        self._file_path = None

    def __str__(self):
        return "{0} by {1} ({2})".format(self._name, self._artist, self._url)

    @corrupt_if_none
    def _download_link(self):
        return find_first(r'"(https://freemusicarchive\.org/music/download/[\d\w]+?)"', self._track_page)

    @corrupt_if_none
    def _get_info(self):
        return find_first(r'<title>Free Music Archive: (.+) - (.+)</title>', self._track_page)
        
    def save(self, file_path):
        with open(file_path, 'wb') as f:
            f.write(self._data)
        self._file_path = file_path

    def artist(self):
        return self._artist
    def name(self):
        return self._name
    def url(self):
        return self._url
    def file_path(self):
        if self._file_path is None:
            return None
        return os.path.abspath(self._file_path)



PER_PAGE = 10
ALL_SONGS = "http://freemusicarchive.org/genre/{0}/?sort=track_date_published&d=1&page={1}&per_page=" + str(PER_PAGE)


def get_song(genre = 'Electronic'):
    def random_page():
        first_page = get(ALL_SONGS.format(genre, 1))
        num_of_pages = int(find_first(r'</b> of <b>(\d+?)</b>', first_page))/PER_PAGE
        return int(random() * num_of_pages) + 1
    
    def random_song():
        songs_url = ALL_SONGS.format(genre, random_page())
        links = []
        while links == []:
            page = get(songs_url)
            links = re.findall(r'<span class="ptxt-track"><a href="(.+?)">', page)
            links = links[1:] #cut off first link because its just the url of the page
            if links == []:
                print "COULDN'T GET ANY SONG LINKS PROBABLY BECAUSE I'M SPAMMING TOO HARD, sleeping for 10 secs and downloading songs page agian..."
                time.sleep(10)
        track = None
        while track is None: 
            try:
                rand_url = links[int(random()*len(links))]
                track = song(rand_url)
            except corrupt_song_link_exception:
                print "Song link was corrupt! Getting a new song..."
        file_name = 'music\\' + str(random()) + '.mp3'
        track.save(file_name)
        return track
    
    return random_song()




if __name__ == "__main__":
    while 1:
        s = get_song('dubstep')
        print s
                        




'''
    def parse_page(page):
        return re.findall(r'"(https://freemusicarchive\.org/music/download/[\d\w]+?)"', page)

    def save_song(url):
        data = get(url)
        file_name = 'music\\' + str(random()) + '.mp3'
        with open(file_name, 'wb') as f:
            f.write(data)
        return os.path.abspath(file_name)

    def rand_song():
        all_urls = parse_page(get(ALL_SONGS))
        rand_url = all_urls[int(random()*len(all_urls))]
        return save_song(rand_url)
    '''
    
