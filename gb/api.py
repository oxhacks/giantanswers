import os
from collections import namedtuple
from datetime import datetime

import requests
import humanize
from fuzzywuzzy import process


Answer = namedtuple('Answer', ['deck', 'name', 'release', 'release_human', 'match'])


def parse_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")


def find_match(data, title):
    names = [entry['name'] for entry in data]
    match = process.extractOne(title, names)
    for entry in data:
        if entry['name'] == title:
            release = parse_date(data[0]['original_release_date'])
            release_human = humanize.naturaltime(release)
            return Answer(
                deck=entry['deck'],
                name=entry['name'],
                release=release,
                release_human=release_human,
                match=True
            )
    return Answer(
        name=title,
        deck="No entry available",
        release=None,
        release_human=None,
        match=False
    )


class GBApi(object):
    def __init__(self, protocol='https', format='json'):
        self.protocol = protocol
        self.domain = 'www.giantbomb.com'
        self.api_key = os.environ.get('GB_API_KEY')
        self.format = 'json'
        self.fields = ['name', 'original_release_date', 'deck']
        self.headers = {'User-Agent': 'Giant Answers/1.0'}

    def build_url(self, resource):
        return "{}://{}/api/{}".format(self.protocol, self.domain, resource)

    def whatis(self, title):
        _filter = "name:{}".format(title)
        _fields = ','.join(self.fields)
        params = {
            'api_key': self.api_key,
            'format': self.format,
            'field_list': _fields,
            'filter': _filter
        }
        url = self.build_url('games')
        req = requests.get(url, params=params, headers=self.headers)
        print("sending request to {}".format(req.url))
        data = req.json()['results']
        match = find_match(data, title)
        return match