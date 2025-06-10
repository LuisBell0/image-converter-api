from django.contrib.auth import get_user_model
from rest_framework import status
import json

from images.tests.test_setup import TestSetUp

User = get_user_model()

# TODO: ADD MORE TESTS AND CHECKS


# Create your tests here.
class ImagesTestCase(TestSetUp):

    def test_image_conversion_by_authenticated_user(self):
        user = User.objects.create(
            email=self.user_data['email'],
            username=self.user_data['username'],
            password=self.user_data['password']
        )

        self.client.force_authenticate(user=user)

        config = json.dumps({
            "format": "png"
        })
        data = {
            "image": self.image,
            "config": config,
        }

        response = self.client.post(self.transform_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_image_conversion_by_non_authenticated_user(self):
        image_file = self.image
        config = json.dumps({
            "format": "png"
        })

        data = {
            "image": self.image,
            "config": config,
        }

        response = self.client.post(self.transform_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        