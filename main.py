import json
import os
import time

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
    print('Sending %s to Discord' % card.url)
    payload = {
        "content": "New card posted!",
        "embeds": [
            {
                "title": card.title,
                "description": f'{card.text}' if not card.flavor else f'{card.text}\n_{card.flavor}',
                "url": card.url,
                # "color": null,
                "fields": [
                    {
                    "name": "Mana Cost",
                    "value": card.cost,
                    "inline": True
                    },
                    {
                    "name": "Type",
                    "value": card.type,
                    "inline": True
                    },
                    {
                    "name": "Power/Toughness",
                    "value": card.pt,
                    "inline": True
                    }
                ],
                "image": {
                    "url": card.image_url
                }
            }
        ]
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    response.raise_for_status()


def main():
    while True:
        last_card = get_last_card()
        spoiler = MythicSpoiler()
        cards = spoiler.get_latest_cards(last_card)
        if cards:
            for card in cards:
                send_to_discord(card)
            save_last_card(cards[0].url)
        else:
            print('No new cards found')
        time.sleep(TIMER)

main()