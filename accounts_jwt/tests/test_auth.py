from django.contrib.auth import get_user_model
from rest_framework import status

from accounts_jwt.tests.test_setup import TestSetUp

# Create your tests here.

User = get_user_model()


# TODO: ADD MORE TESTS AND CHECKS
class TestViews(TestSetUp):
    def test_user_login_with_valid_credentials(self):
        User.objects.create_user(
            email=self.user_data["email"],
            username=self.user_data["username"],
            password=self.user_data["password"]
        )

        response = self.client.post(path=self.login_url,
                                    data={'email': self.user_data["email"],
                                          'password': self.user_data["password"]
                                          })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_with_empty_credentials(self):
        response = self.client.post(path=self.login_url,
                                    data={'email': '',
                                          'password': '',
                                          })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_non_existing_credentials(self):
        response = self.client.post(path=self.login_url,
                                    data={'email': self.user_data["email"],
                                          'password': self.user_data["password"]
                                          })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_register_with_valid_credentials(self):
        response = self.client.post(path=self.register_url,
                                    data={'email': self.user_data["email"],
                                          'username': self.user_data["username"],
                                          'password': self.user_data["password"],
                                          're_password': self.user_data["password"],
                                          })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_register_with_missing_fields(self):
        response = self.client.post(self.register_url, {
            'email': '',
            'username': '',
            'password': '',
            're_password': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_with_mismatched_passwords(self):
        response = self.client.post(self.register_url, {
            'email': self.user_data['email'],
            'username': self.user_data['username'],
            'password': 'password123',
            're_password': 'password321'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_with_existing_email(self):
        User.objects.create_user(
            email=self.user_data['email'],
            username='anotheruser',
            password=self.user_data['password']
        )
        response = self.client.post(self.register_url, {
            'email': self.user_data['email'],
            'username': self.user_data['username'],
            'password': self.user_data['password'],
            're_password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
