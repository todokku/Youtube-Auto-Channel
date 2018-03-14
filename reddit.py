import requests as req
import re
from get import get as good_get
from util import find_first, parse

class post():
    def __init__(self, url, title, is_sticky):
        self.url = url
        self.title = title
        self.is_sticky = is_sticky


class subreddit():

    def __init__(self, name):
        self.name = name

    def _get(self, url):
        return good_get(url).content

    def _parse_links(self, content):
        blocks = re.findall(r'<a class="title.+?comments?</a>', content)
        posts = []
        last_post = ''
        for b in blocks:
            url = find_first('href="(.+?)"', b)
            if url[:2] == '/r': #if it's in internal url
                before_post = parse(content, last_post, b)
                url = find_first(r'data-url="(.+?)" data-permalink', before_post)
            title = find_first(r'rel="(?:nofollow)?" >(.+?)</a', b)
            title = ''.join(c for c in title if ord(c) <= 127) #ELIMINATES ALL UTF-8 ENCODED NON-ASCII CHARACTERS
            is_sticky = '<span class="stickied-tagline"' in b
            posts.append(post(url, title, is_sticky))
            last_post = b
        return posts

    def _get_links(self, url):
        return self._parse_links(self._get(url))

    def hot(self):
        return self._get_links('https://www.reddit.com/r/' + self.name)

    def top(self, of = 'all'):
        of = of.lower()
        if of not in ['all', 'day', 'week', 'month', 'year']:
            raise ValueError("Can only get top of all, day, week, month or year, not " + of)
        base_url = 'https://www.reddit.com/r/' + self.name + '/top/?sort=top&t='
        return self._get_links(base_url + of)


if __name__ == "__main__":
    le = subreddit('dankmemes').hot()
                               
