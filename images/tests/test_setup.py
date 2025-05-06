import json

from django.urls import reverse
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    def setUp(self):
        self.image_url = reverse('image-list')

        self.user_data = {
            'email': 'test@test.com',
            'username': 'test',
            'password': 'testpassword'
        }
        self.config = json.dumps({
            "optimize": 80,
            "resize": {
                "width": 800,
                "height": 1000,
            },
            "format": "png",
            "crop": {
                "upper": 50,
                "right": 300,
                "left": 50,
                "lower": 300,
            },
        }),
        return super().setUp()
