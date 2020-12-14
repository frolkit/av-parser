from rest_framework.test import APIClient
from django.test import TestCase

from .models import Location


class ItemCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.query = 'Куртка'
        cls.location = 'Москва'
        cls.location_id = '637640'
        cls.response_post = cls.client.post("/add/",
                                            {'query': cls.query,
                                             'location': cls.location})

    def test_post_request_correct(self):
        self.assertEqual(self.response_post.status_code, 201)
        self.assertEqual(self.response_post.content, b'1')

    def test_get_item_correct(self):
        response = self.client.get("/stat/", {'id': 1,
                                              'start': 1,
                                              'stop': 9999999999})
        self.assertEqual(response.status_code, 200)

    def test_get_ads(self):
        response = self.client.get("/top/", {'id': 1})
        self.assertEqual(response.status_code, 200)

    def test_create_location(self):
        location = Location.objects.get(title=self.location)
        self.assertEqual(self.location_id, str(location.location_id))


class ErrorTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def test_create_item_bad_request(self):
        response = self.client.post("/add/")
        self.assertEqual(response.status_code, 400)

    def test_create_item_bad_location(self):
        response = self.client.post("/add/", {'query': 'Куртка',
                                              'location': "Масква"})
        self.assertEqual(response.status_code, 404)

    def test_stat_error_test(self):
        response = self.client.get("/stat/", {'id': 1})
        self.assertEqual(response.status_code, 404)

    def test_top_error_test(self):
        response = self.client.get("/top/", {'id': 1})
        self.assertEqual(response.status_code, 404)
