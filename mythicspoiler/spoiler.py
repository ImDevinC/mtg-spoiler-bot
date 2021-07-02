import requests
from bs4 import BeautifulSoup

from .card import MythicSpoilerCard

class MythicSpoiler:
    def __init__(self):
        self._url = 'https://mythicspoiler.com/'
        self._spoiler_url = 'newspoilers.html'

    def get_latest_cards(self, last_card = ''):
        response = requests.get('%s%s' % (self._url, self._spoiler_url))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', class_='grid-card')
        card_list = []
        for card in cards:
            card_url = MythicSpoilerCard.get_card_url(card)
            full_url = '%s%s' % (self._url, card_url)
            if full_url == last_card:
                break
            card_list.append(MythicSpoilerCard(full_url))
        return card_list
        
        
        