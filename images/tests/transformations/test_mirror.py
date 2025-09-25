from rest_framework import status
from rest_framework.response import Response

from ..test_setup import TestSetUp

class TestMirror(TestSetUp):
    """
    Test suite for the `mirror` image transformation.
    """
    def test_mirror_successful_with_empty_dictionary(self) -> None:
        """
        Applying mirror with an empty dictionary should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "mirror": {}
        }
        self.post_transformation(config_dict=configuration)

    def test_mirror_successful_with_empty_list(self) -> None:
        """
        Applying mirror with an empty list should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "mirror": []
        }
        self.post_transformation(config_dict=configuration)

    def test_mirror_successful_with_none_value(self) -> None:
        """
        Applying mirror with a None value should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "mirror": None
        }
        self.post_transformation(config_dict=configuration)

    def test_mirror_unsuccessful_with_non_empty_dictionary(self) -> None:
        """
        Providing a non-empty dictionary for mirror should return HTTP 400 with a message indicating that parameters are not accepted.
        """
        configuration: dict = {
            "mirror": {"key": "value"}
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("does not accept parameters", detail_message)

    def test_mirror_unsuccessful_invalid_type(self) -> None:
        """
        Providing an invalid type (boolean) for mirror should return HTTP 400 with a type error message.
        """
        configuration: dict = {
            "mirror": True
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("does not accept parameters", detail_message)

        configuration: dict = {
            "mirror": 12
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("does not accept parameters", detail_message)
