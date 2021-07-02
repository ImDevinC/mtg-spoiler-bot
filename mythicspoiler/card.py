import re

import requests
from bs4 import BeautifulSoup, Comment

class MythicSpoilerCard:
    def __init__(self, url):
        self._url = url
        self._image_url = re.sub('.html$', '.jpg', url)
        self._title = ''
        self._cost = ''
        self._type = ''
        self._text = ''
        self._flavor_text = ''
        self._illustrator = ''
        self._pt = ''
        self._get_card_details()

    @property
    def url(self):
        return self._url

    @property
    def image_url(self):
        return self._image_url

    @property
    def title(self):
        return self._title

    @property
    def cost(self):
        return self._cost

    @property
    def type(self):
        return self._type

    @property
    def text(self):
        return self._text

    @property
    def flavor(self):
        return self._flavor_text

    @property
    def illustrator(self):
        return self._illustrator

    @property
    def pt(self):
        return self._pt

    
    def _get_card_details(self):
        response = requests.get(self._url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        card_table = tables[6]
        rows = card_table.find_all('tr')
        for row in rows:
            comments = row.find_all(text=lambda text: isinstance(text, Comment))
            for comment in comments:
                comment_text = comment.extract()
                string_data = row.text.strip()
                if comment_text == 'CARD NAME':
                    self._title = string_data
                elif comment_text == 'MANA COST':
                    self._cost = string_data
                elif comment_text == 'TYPE':
                    self._type = string_data
                elif comment_text == 'CARD TEXT' and string_data:
                    self._text = string_data
                elif comment_text == 'FLAVOR TEXT':
                    self._flavor_text = string_data
                elif comment_text == 'ILLUS':
                    self._illustrator = row.find('font', size=1).text.strip()
                elif comment_text == 'P/T':
                    self._pt = row.find('font', size=2).text.strip()
    
    @staticmethod
    def get_card_url(card):
        link = card.find('a')
        return link.get('href').strip()