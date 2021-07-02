import json
import os
import time
import logging

import requests

from mythicspoiler.spoiler import MythicSpoiler

WEBHOOK_URL = os.environ['WEBHOOK_URL']
TIMER = os.environ.get('TIMER', 300)
CARD_JSON = os.environ.get('CARD_JSON', '/tmp/cards/card.json')

def get_last_card():
    data = {}
    try:
        with open(CARD_JSON, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        pass
    return data.get('last_card')

def save_last_card(card):
    with open(CARD_JSON, 'w+') as f:
        json.dump({'last_card': card}, f)

def send_to_discord(card):
    logging.info('Sending %s to discord', card.url)
    fields = []
    if card.cost:
        fields.append({
            'name': 'Mana cost',
            'value': card.cost,
            'inline': True
        })
    if card.type:
        fields.append({
            'name': 'Type',
            'value': card.type,
            'inline': True
        })
    if card.pt:
        fields.append({
            'name': 'Power/Toughness',
            'value': card.pt,
            'inline': True
        })
    payload = {
        'content': 'New card posted!',
        'embeds': [
            {
                "title": card.title,
                "description": f'{card.text}' if not card.flavor else f'{card.text}\n_{card.flavor}',
                'url': card.url,
                'fields': fields,
                'image': {
                    'url': card.image_url
                }
            }
        ]
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    response.raise_for_status()


def main():
    logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))
    while True:
        last_card = get_last_card()
        spoiler = MythicSpoiler()
        logging.info('Getting cards')
        cards = spoiler.get_latest_cards(last_card)
        if cards:
            for card in cards:
                try:
                    send_to_discord(card)
                except Exception as ex:
                    logging.error('Failed to send %s.\nERROR: %s\n\n%s', card.url, ex, json.dumps(card.url))
            save_last_card(cards[0].url)
        else:
            logging.info('No new cards found')
        time.sleep(TIMER)

main()