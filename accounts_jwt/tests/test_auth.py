from django.contrib.auth import get_user_model
from rest_framework import status

from accounts_jwt.tests.test_setup import TestSetUp

User = get_user_model()


class TestViews(TestSetUp):
    def test_user_login_with_valid_credentials(self):
        # Create a user first
        User.objects.create_user(
            email=self.user_data["email"],
            username=self.user_data["username"],
            password=self.user_data["password"]
        )

        response = self.client.post(
            path=self.login_url,
            data={
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect both access and refresh tokens in response
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login_with_empty_credentials(self):
        response = self.client.post(
            path=self.login_url,
            data={"email": "", "password": ""},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Expect error details about missing fields
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)

    def test_user_login_non_existing_credentials(self):
        response = self.client.post(
            path=self.login_url,
            data={
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Expect an error message indicating invalid credentials
        self.assertIn("detail", response.data)

    def test_user_login_with_incorrect_password(self):
        # Create a user with a known password
        User.objects.create_user(
            email=self.user_data["email"],
            username=self.user_data["username"],
            password=self.user_data["password"],
        )

        # Attempt login with correct email but wrong password
        response = self.client.post(
            path=self.login_url,
            data={"email": self.user_data["email"], "password": "wrongpass"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_login_returns_jwt_tokens(self):
        # Ensure login returns both access and refresh tokens
        User.objects.create_user(
            email=self.user_data["email"],
            username=self.user_data["username"],
            password=self.user_data["password"],
        )
        response = self.client.post(
            path=self.login_url,
            data={
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        # Tokens should be non-empty strings
        self.assertIsInstance(response.data["access"], str)
        self.assertIsInstance(response.data["refresh"], str)

    def test_refresh_token(self):
        # Create user and log in to obtain refresh token
        User.objects.create_user(
            email=self.user_data["email"],
            username=self.user_data["username"],
            password=self.user_data["password"],
        )
        login_response = self.client.post(
            path=self.login_url,
            data={
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
        )
        refresh_token = login_response.data.get("refresh")
        self.assertIsNotNone(refresh_token)

        # Use refresh endpoint to get a new access token
        response = self.client.post(
            path=self.refresh_url,
            data={"refresh": refresh_token},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIsInstance(response.data["access"], str)

    def test_get_current_user(self):
        # Create user and log in to obtain access token
        user = User.objects.create_user(
            email=self.user_data["email"],
            username=self.user_data["username"],
            password=self.user_data["password"],
        )
        login_response = self.client.post(
            path=self.login_url,
            data={
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
        )
        access_token = login_response.data.get("access")
        self.assertIsNotNone(access_token)

        # Authenticate client with access token and retrieve user info
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(self.user_me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify returned user details
        self.assertEqual(response.data.get("email"), self.user_data["email"])
        self.assertEqual(response.data.get("username"), self.user_data["username"])

    def test_user_register_with_valid_credentials(self):
        response = self.client.post(
            path=self.register_url,
            data={
                "email": self.user_data["email"],
                "username": self.user_data["username"],
                "password": self.user_data["password"],
                "re_password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Confirm user was created in database
        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

    def test_user_register_with_missing_fields(self):
        response = self.client.post(
            path=self.register_url,
            data={"email": "", "username": "", "password": "", "re_password": ""},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Expect error details for each missing field
        self.assertIn("email", response.data)
        self.assertIn("username", response.data)
        self.assertIn("password", response.data)
        self.assertIn("re_password", response.data)

    def test_user_register_with_mismatched_passwords(self):
        response = self.client.post(
            path=self.register_url,
            data={
                "email": self.user_data["email"],
                "username": self.user_data["username"],
                "password": "mismatchpassword123",
                "re_password": "mismatchpassword321",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Expect a non-field error indicating password mismatch
        self.assertIn("non_field_errors", response.data)

    def test_user_register_with_existing_email(self):
        User.objects.create_user(
            email=self.user_data["email"],
            username="anotheruser",
            password=self.user_data["password"],
        )
        response = self.client.post(
            path=self.register_url,
            data={
                "email": self.user_data["email"],
                "username": self.user_data["username"],
                "password": self.user_data["password"],
                "re_password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Expect an error indicating email already in use
        self.assertIn("email", response.data)

    def test_user_register_with_existing_username(self):
        User.objects.create_user(
            email="other@example.com",
            username=self.user_data["username"],
            password=self.user_data["password"],
        )
        response = self.client.post(
            path=self.register_url,
            data={
                "email": self.user_data["email"],
                "username": self.user_data["username"],
                "password": self.user_data["password"],
                "re_password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Expect an error indicating username already in use
        self.assertIn("username", response.data)
