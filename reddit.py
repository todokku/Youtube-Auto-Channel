import requests as req
import re
from get import get as good_get


class subreddit():

    def __init__(self, name):
        self.name = name

    def _get(self, url): #GIVE THIS SOME ERROR HANDLING
        return good_get(url).content

    def _parse_links(self, content):
        return re.findall('data-url="(.+?)"', content)

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
                               
