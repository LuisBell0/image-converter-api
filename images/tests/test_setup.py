import json
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    def setUp(self):
        self.transform_url = reverse('image-list')

        self.user_data = {
            'email': 'test@test.com',
            'username': 'test',
            'password': 'testpassword'
        }
        self.image = self.generate_test_image()
        super().setUp()

    def generate_test_image(self):
        image_io = BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        return ContentFile(image_io.getvalue(), name="test_image.jpg")

    def post_transformation(self, config_dict: dict, image=None, expected_status=status.HTTP_200_OK) -> Response:
        """
        Helper to post a transformation request and assert status.
        Returns the response object for further inspection.
        """
        upload_file = image or self.image
        upload_file.seek(0)
        payload = {
            "config": json.dumps(config_dict),
            "image": upload_file
        }
        response = self.client.post(self.transform_url, payload, format="multipart")
        self.assertEqual(response.status_code, expected_status)
        return response
