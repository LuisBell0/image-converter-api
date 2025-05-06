from django.urls import reverse
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('customuser-list')
        self.login_url = reverse('jwt-create')
        self.refresh_url = reverse('jwt-refresh')
        self.verify_url = reverse('jwt-verify')

        self.user_data = {
            'email': 'test@test.com',
            'username': 'test',
            'password': 'testpassword'
        }
        return super().setUp()
