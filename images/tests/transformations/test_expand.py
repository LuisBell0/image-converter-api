from rest_framework import status
from rest_framework.response import Response

from ..test_setup import TestSetUp


class TestExpand(TestSetUp):
    """
    Test suite for the `expand` image transformation.
    """

    def test_expand_successful_values(self) -> None:
        """
        Applying expand with valid fill formats (hex color, RGBA tuple, integer) should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "expand": {
                "border": 10,
                "fill": "#ffffff",
            }
        }
        self.post_transformation(config_dict=configuration)

        configuration = {
            "expand": {
                "border": 10,
                "fill": (255, 0, 0, 0),
            }
        }
        self.post_transformation(config_dict=configuration)

        configuration = {
            "expand": {
                "border": 10,
                "fill": 10,
            }
        }
        self.post_transformation(config_dict=configuration)

    def test_expand_extra_keys_do_not_crash(self) -> None:
        """
        Including unexpected keys in expand configuration (e.g., 'foo') should not cause a server error and return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "expand": {
                "border": 10,
                "fill": 10,
                "foo": "bar"
            }
        }
        self.post_transformation(config_dict=configuration)

    def test_expand_missing_required_parameters(self) -> None:
        """
        Omitting the required 'border' parameter should return HTTP 400 with a message indicating the missing key.
        """
        configuration: dict = {
            "expand": {
                "fill": 1,
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("missing required configuration key", detail_message)

    def test_expand_unsuccessful_with_invalid_types(self) -> None:
        """
        Providing invalid types for 'border' (string) and 'fill' (boolean) should return HTTP 400 with type error messages.
        """
        configuration: dict = {
            "expand": {
                "border": "true"
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)

        configuration = {
            "expand": {
                "border": 1,
                "fill": True,
            }
        }
        response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)

    def test_expand_unsuccessful_with_invalid_color_string(self) -> None:
        """
        Supplying an unsupported string for 'fill' should return HTTP 400 with an unknown color specifier error.
        """
        configuration: dict = {
            "expand": {
                "border": 1,
                "fill": "True",
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("unknown color specifier", detail_message)

    def test_expand_unsuccessful_with_out_of_range_border(self) -> None:
        """
        Using a negative value for 'border' should return HTTP 400 with an out of range error message.
        """
        configuration: dict = {
            "expand": {
                "border": -1,
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("out of range", detail_message)
