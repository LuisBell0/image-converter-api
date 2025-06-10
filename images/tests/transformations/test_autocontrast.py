from rest_framework import status
from rest_framework.response import Response

from ..test_setup import TestSetUp


#TODO: FIX OUT OF RANGE AND INVALID TYPES

class TestAutocontrast(TestSetUp):
    """
    Test suite for the `autocontrast` image transformation endpoint.
    """

    def test_autocontrast_success_default(self) -> None:
        """
        Applying autocontrast with valid default parameters should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "autocontrast": {
                "cutoff": 10.0,
                "ignore": 1,
                "preserve_tone": True
            }
        }
        self.post_transformation(config_dict=configuration)

    def test_autocontrast_extra_keys_do_not_crash(self) -> None:
        """
        Including unexpected keys in autocontrast configuration should not cause a server error.
        """
        configuration: dict = {
            "autocontrast": {
                "cutoff": 10.0,
                "ignore": 1,
                "preserve_tone": True,
                "foo": "bar"
            }
        }
        self.post_transformation(config_dict=configuration)

    def test_autocontrast_missing_required_parameters(self) -> None:
        """
        Omitting required autocontrast parameters should return HTTP 400 with a descriptive message.
        """
        configuration: dict = {
            "autocontrast": {
                "ignore": 1,
                "preserve_tone": True
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("missing", detail_message)

    def test_autocontrast_invalid_types(self) -> None:
        """
        Providing invalid types for autocontrast parameters should return HTTP 400 with type error descriptions.
        """
        configuration: dict = {
            "autocontrast": {
                "cutoff": "high",
                "ignore": 1,
                "preserve_tone": True
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)

        configuration: dict = {
            "autocontrast": {
                "cutoff": 10.0,
                "ignore": 1.5,
                "preserve_tone": True
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)

        configuration: dict = {
            "autocontrast": {
                "cutoff": 10.0,
                "ignore": 1,
                "preserve_tone": "yes"
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)

    def test_autocontrast_out_of_range(self) -> None:
        """
        Autocontrast parameters outside allowed ranges should return HTTP 400 with range error descriptions.
        """
        configuration: dict = {
            "autocontrast": {
                "cutoff": -1.0,
                "ignore": 1,
                "preserve_tone": True
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("out of range", detail_message)

        configuration: dict = {
            "autocontrast": {
                "cutoff": 10.0,
                "ignore": -1,
                "preserve_tone": True
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("out of range", detail_message)

        configuration: dict = {
            "autocontrast": {
                "cutoff": 101.0,
                "ignore": 1,
                "preserve_tone": True
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("out of range", detail_message)
