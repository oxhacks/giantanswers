"""Interact with the Giant Bomb API."""

import os
from collections import namedtuple
from datetime import datetime

import requests
import humanize
from fuzzywuzzy import process

import helpers

# This helps tidy up the results returned
Answer = namedtuple('Answer', ['deck', 'name', 'release', 'release_human', 'match'])


def parse_date(date_string):
    """Parse the date string from the database into a `datetime` object.

    :param date_string: the raw date string to parse
    :returns: the `datetime` version of the given date string

    """
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")


def find_match(data, title):
    """Parse the list of search results to find the best match.
    This uses LDA to compare titles against each other.

    :param data: the iterable of response data to search through
    :param title: the title to compare the result set against
    :returns: an `Answer` `namedtuple` holding the best match

    """
    names = [entry['name'] for entry in data]
    try:
        match, score = process.extractOne(title, names)
    except TypeError as exc:
        print("no match found: {}".format(exc))
    if data and match:
        print("matched {} with score of {}".format(match, score))
        for entry in data:
            if entry['name'] == match:
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
    """Class to facilitate interaction."""
    def __init__(self, protocol='https', format='json'):
        """Initialize the helper.

        :param protocol: likely either `http` or `https`. Use `https` unless you're crazy.
        :param format`: the format to grab the results in - either `xml` or `json`
        :returns: `None`

        """
        self.protocol = protocol
        self.domain = 'www.giantbomb.com'
        self.api_key = os.environ.get('GB_API_KEY')
        self.format = 'json'
        self.fields = ['name', 'original_release_date', 'deck']
        self.headers = {'User-Agent': 'Giant Answers/1.0'}

    def build_url(self, resource):
        """Build the URL against the given resource.

        :param resource: the resource (like `games`) that calls should be fired against
        :returns: the URL string to use

        """
        return "{}://{}/api/{}".format(self.protocol, self.domain, resource)

    def whatis(self, raw_title):
        """Search the API for the given title.
        
        :param raw_title: the raw spoken title string to search four
        :returns: the best match from the API given the params
        
        """
        print("Searching for {}".format(raw_title))
        title = helpers.word_to_int(raw_title)
        print("fixed title to {}".format(title))
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
        print("response: ", req.json())
        match = find_match(data, title)
        return match