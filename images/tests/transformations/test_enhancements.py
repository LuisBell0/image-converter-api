from rest_framework import status
from rest_framework.response import Response

from ..test_setup import TestSetUp

class TestEnhancemenets(TestSetUp):
    """
    Test suite for the image enhancement: `brightness`, `contrast`, `sharpness`, and `color`.
    """

    def test_enhancement_successful_as_int(self) -> None:
        """
        Applying brightness enhancement with an integer factor should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "brightness": 3
        }
        self.post_transformation(config_dict=configuration)

    def test_enhancement_successful_as_float(self) -> None:
        """
        Applying sharpness enhancement with a float factor should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "sharpness": 3.3
        }
        self.post_transformation(config_dict=configuration)

    def test_enhancement_invalid_type(self) -> None:
        """
        Providing an invalid type (string) for color enhancement should return HTTP 400 with a type error message.
        """
        configuration: dict = {
            "color": "3",
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)

    def test_enhancement_out_of_range(self) -> None:
        """
        Providing an out-of-range value for contrast enhancement should return HTTP 400 with a range error message.
        """
        configuration: dict = {
            "contrast": -1,
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("out of range", detail_message)
