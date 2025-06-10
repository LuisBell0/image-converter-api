from rest_framework import status
from rest_framework.response import Response

from ..test_setup import TestSetUp


class TestBorderCrop(TestSetUp):
    """
    Test suite for the `border_crop` image transformation.
    """

    def test_border_crop_successful_with_required_parameter(self) -> None:
        """
        Applying border_crop with only the required parameter returns HTTP 200 for anonymous users.
        """
        configuration: dict = {"border_crop": 10}
        self.post_transformation(config_dict=configuration, expected_status=status.HTTP_200_OK)

    def test_border_crop_invalid_value_type(self) -> None:
        """
        Providing a non-integer crop value returns HTTP 400.
        """
        configuration: dict = {"border_crop": "ten"}
        response: Response = self.post_transformation(config_dict=configuration, expected_status=status.HTTP_400_BAD_REQUEST)
        detail_message: str = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)
