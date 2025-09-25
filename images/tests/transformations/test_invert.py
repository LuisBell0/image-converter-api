from rest_framework import status
from rest_framework.response import Response

from ..test_setup import TestSetUp

class TestInvert(TestSetUp):
    """
    Test suite for the `invert` image transformation.
    """
    def test_invert_successful_with_empty_dictionary(self) -> None:
        """
        Applying equalize with an empty dictionary should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "invert": {}
        }
        self.post_transformation(config_dict=configuration)

    def test_invert_successful_with_empty_list(self) -> None:
        """
        Applying invert with an empty list should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "invert": []
        }
        self.post_transformation(config_dict=configuration)

    def test_invert_successful_with_none_value(self) -> None:
        """
        Applying invert with a None value should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "invert": None
        }
        self.post_transformation(config_dict=configuration)

    def test_invert_unsuccessful_with_non_empty_dictionary(self) -> None:
        """
        Providing a non-empty dictionary for invert should return HTTP 400 with a message indicating that parameters are not accepted.
        """
        configuration: dict = {
            "invert": {"key": "value"}
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("does not accept parameters", detail_message)

    def test_invert_unsuccessful_invalid_type(self) -> None:
        """
        Providing an invalid type (boolean) for invert should return HTTP 400 with a type error message.
        """
        configuration: dict = {
            "invert": True
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("does not accept parameters", detail_message)

        configuration: dict = {
            "invert": 12
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("does not accept parameters", detail_message)
