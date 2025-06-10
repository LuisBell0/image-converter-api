import json
from rest_framework import status
from ..test_setup import TestSetUp


class TestBorderCrop(TestSetUp):
    """
    Tests for the border_crop transformation.
    """

    def test_border_crop_successful_with_threshold_only(self) -> None:
        """
        Applying border_crop with only the required threshold returns HTTP 200.
        """
        configuration = {"threshold": 10}
        data = {
            "config": json.dumps(configuration),
            "image": self.image
        }
        response = self.client.post(self.transform_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_border_crop_successful_with_all_parameters(self) -> None:
        """
        Applying border_crop with threshold and optional edges returns HTTP 200.
        """
        configuration = {
            "threshold": 12,
            "top": 2,
            "bottom": 3,
            "left": 4,
            "right": 5
        }
        data = {
            "config": json.dumps(configuration),
            "image": self.image
        }
        response = self.client.post(self.transform_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_border_crop_missing_threshold_returns_bad_request(self) -> None:
        """
        Omitting the required threshold parameter returns HTTP 400.
        """
        configuration = {"top": 2, "bottom": 2, "left": 2, "right": 2}
        data = {
            "config": json.dumps(configuration),
            "image": self.image
        }
        response = self.client.post(self.transform_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_border_crop_invalid_threshold_type_returns_bad_request(self) -> None:
        """
        Providing a non-integer threshold returns HTTP 400.
        """
        configuration = {"threshold": "ten"}
        data = {
            "config": json.dumps(configuration),
            "image": self.image
        }
        response = self.client.post(self.transform_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_border_crop_invalid_optional_parameter_type_returns_bad_request(self) -> None:
        """
        Providing wrong type for an optional edge parameter returns HTTP 400.
        """
        configuration = {"threshold": 10, "top": "two"}
        data = {
            "config": json.dumps(configuration),
            "image": self.image
        }
        response = self.client.post(self.transform_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_border_crop_with_extra_keys_does_not_crash(self) -> None:
        """
        Including unexpected keys does not cause server error.
        """
        configuration = {"threshold": 10, "unexpected": True}
        data = {
            "config": json.dumps(configuration),
            "image": self.image
        }
        response = self.client.post(self.transform_url, data, format="multipart")
        self.assertIn(response.status_code, (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST))

    def test_border_crop_missing_config_key_returns_bad_request(self) -> None:
        """
        Omitting the config field returns HTTP 400.
        """
        data = {"image": self.image}
        response = self.client.post(self.transform_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
