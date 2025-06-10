from rest_framework import status
from rest_framework.response import Response

from ..test_setup import TestSetUp


class TestContain(TestSetUp):
    """
    Test suite for the `contain` image transformation.
    """

    def test_contain_with_all_parameters_successful(self) -> None:
        """
        Sending all valid parameters for `contain` should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "contain": {
                "size": (4, 4),
                "method": "BILINEAR"
            }
        }
        self.post_transformation(config_dict=configuration)

    def test_contain_only_required_parameters_successful(self) -> None:
        """
        Sending only the required `size` parameter for `contain` should return HTTP 200 for anonymous users.
        """
        configuration: dict = {
            "contain": {
                "size": (4, 4),
            }
        }
        self.post_transformation(config_dict=configuration)

    def test_contain_unexpected_keys_do_not_crash(self) -> None:
        """
        Including unexpected keys in `contain` configuration should not raise server errors.
        """
        configuration: dict = {
            "contain": {
                "size": (4, 4),
                "method": "BILINEAR",
                "key": "unexpected"
            }
        }
        self.post_transformation(config_dict=configuration)

    def test_contain_missing_required_parameters(self) -> None:
        """
        Omitting the required `size` parameter for `contain` should return HTTP 400 with a descriptive message.
        """
        configuration: dict = {
            "contain": {
                "method": "BILINEAR"
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("missing", detail_message)
        self.assertIn("key", detail_message)

    def test_contain_invalid_types(self) -> None:
        """
        Providing invalid types for `size` and `method` should return HTTP 400 with type error description.
        """
        configuration: dict = {
            "contain": {
                "size": "(4, 4)",
                "method": 2
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)

    def test_contain_invalid_method(self) -> None:
        """
        Providing an unsupported `method` value should return HTTP 400 with choice error description.
        """
        configuration: dict = {
            "contain": {
                "size": (4, 4),
                "method": "UNKNOWN"
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("contain 'method' must be one of", detail_message)

    def test_contain_invalid_tuple(self) -> None:
        """
        Providing a tuple of incorrect length for `size` should return HTTP 400 with dimensional error.
        """
        configuration: dict = {
            "contain": {
                "size": (4, 4, 4, 4),
            }
        }
        response: Response = self.post_transformation(
            config_dict=configuration,
            expected_status=status.HTTP_400_BAD_REQUEST
        )
        detail_message: str = response.data.get("detail", "")
        self.assertIn("must be a tuple of 2 ints", detail_message)
