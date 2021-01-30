import requests
from rest_framework import serializers
from rest_framework.exceptions import (Throttled,
                                       NotAuthenticated,
                                       NotFound)

from av_parser.settings import AVITO_AUTH_KEY
from .models import Location, ItemHistory, Ad


class ItemSerializer(serializers.Serializer):
    query = serializers.CharField()
    location = serializers.CharField()

    def request_location_id(self, title: str):
        url = 'https://m.avito.ru/api/1/slocations/'
        params_data = {
            'key': AVITO_AUTH_KEY,
            'q': title,
            'limit': 10
            }
        response = requests.get(url, params=params_data)
        if response.status_code == 403:
            raise NotAuthenticated()
        if response.status_code == 429:
            raise Throttled()
        location_list = response.json()['result']['locations']
        for location in location_list:
            if location['names']['1'] == title:
                location_id = location['id']
                location = Location.objects.create(title=title,
                                                   location_id=location_id)
                return location
        raise NotFound(f"Location {title} not found. Check your input.")

    def get_location_id(self, title: str):
        location = Location.objects.filter(title=title).first()
        if not location:
            location = self.request_location_id(title)
        return location

    def validate(self, data):
        location: str = self.get_location_id(data['location'])
        data['location'] = location
        return data


class ItemHistorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'item', 'number', 'timestamp'
        model = ItemHistory


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'item', 'title', 'location', 'price', 'url'
        model = Ad
