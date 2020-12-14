import requests
import time
from celery import Celery
from rest_framework.exceptions import Throttled

from av_parser.settings import AVITO_AUTH_KEY
from .models import Item, ItemHistory, Ad


app = Celery()


def request_to_avito(item):
    url = 'https://m.avito.ru/api/9/items/'
    post_data = {
        'key': AVITO_AUTH_KEY,
        'query': item.query,
        'locationId': item.location.location_id
        }
    response = requests.get(url, params=post_data)
    if response.status_code == 429:
        raise Throttled()
    response = response.json()['result']
    return response


def create_count_ads(item, response):
    count: int = response['mainCount']
    timestamp: int = response['lastStamp']
    ItemHistory.objects.create(item=item, number=count, timestamp=timestamp)
    return count


def create_ads(item, response):
    ads = response['items'][:5]
    item.ads.all().delete()
    for ad in ads:
        ad = ad['value']
        if ad.get('list'):
            ad = ad['list'][0]['value']
        title = ad['title']
        location = item.location.title
        price = ad['price']
        uri = ad['uri_mweb']
        url = 'https://avito.ru' + uri
        Ad.objects.create(item=item, title=title,
                          location=location, price=price, url=url)


@app.task
def create_stat_and_top(item):
    if type(item) == int:
        item = Item.objects.get(id=item)
    response = request_to_avito(item)
    count = create_count_ads(item, response)
    if count > 0:
        create_ads(item, response)


@app.task
def monitoring_item():
    items = Item.objects.all()
    for item in items:
        create_stat_and_top(item)
        time.sleep(1)
