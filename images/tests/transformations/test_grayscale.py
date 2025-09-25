from rest_framework import status
from rest_framework.response import Response

from ..test_setup import TestSetUp

class TestGrayscale(TestSetUp):
    """
    Test suite for the `grayscale` image transformation.
    """
    def test_grayscale_successful_with_empty_dictionary(self) -> None:
        """
        Applying grayscale with an empty dictionary should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "grayscale": {}
        }
        self.post_transformation(config_dict=configuration)

    def test_grayscale_successful_with_empty_list(self) -> None:
        """
        Applying grayscale with an empty list should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "grayscale": []
        }
        self.post_transformation(config_dict=configuration)

    def test_grayscale_successful_with_none_value(self) -> None:
        """
        Applying grayscale with a None value should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "grayscale": None
        }
        self.post_transformation(config_dict=configuration)

    def test_grayscale_unsuccessful_with_non_empty_dictionary(self) -> None:
        """
        Providing a non-empty dictionary for grayscale should return HTTP 400 with a message indicating that parameters are not accepted.
        """
        configuration: dict = {
            "grayscale": {"key": "value"}
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("does not accept parameters", detail_message)

    def test_grayscale_unsuccessful_invalid_type(self) -> None:
        """
        Providing an invalid type (boolean) for grayscale should return HTTP 400 with a type error message.
        """
        configuration: dict = {
            "grayscale": True
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("does not accept parameters", detail_message)

        configuration: dict = {
            "grayscale": 12
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("does not accept parameters", detail_message)
