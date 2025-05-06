from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import status

from images.tests.test_setup import TestSetUp

User = get_user_model()

# TODO: ADD MORE TESTS AND CHECKS


# Create your tests here.
class ImagesTestCase(TestSetUp):

    def generate_test_image(self):
        image_io = BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        return ContentFile(image_io.getvalue(), name="test_image.jpg")

    def test_image_conversion_by_authenticated_user(self):
        user = User.objects.create(
            email=self.user_data['email'],
            username=self.user_data['username'],
            password=self.user_data['password']
        )

        self.client.force_authenticate(user=user)

        image_file = self.generate_test_image()
        data = {
            "image": image_file,
            "config": self.config,
        }

        response = self.client.post(self.image_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_image_conversion_by_non_authenticated_user(self):
        image_file = self.generate_test_image()
        data = {
            "image": image_file,
            "config": self.config,
        }

        response = self.client.post(self.image_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
