from rest_framework import status
from ..test_setup import TestSetUp
import json
from io import BytesIO
from PIL import Image as PILImage

class TestAutocontrast(TestSetUp):
    """
    Tests for the autocontrast transformation.
    """

    def post_autocontrast(self, config_dict, image=None, expected_status=status.HTTP_200_OK):
        """
        Helper to post an autocontrast request and assert status.
        Returns the response object for further inspection.
        """
        payload = {
            "config": json.dumps(config_dict),
            "image": image or self.image
        }
        response = self.client.post(self.transform_url, payload, format="multipart")
        self.assertEqual(response.status_code, expected_status)
        return response

    def test_autocontrast_success_default(self):
        """
        Full autocontrast config should succeed and return 200.
        """
        config = {"autocontrast": {"cutoff": 10.0, "ignore": 1, "preserve_tone": True}}
        self.post_autocontrast(config)

    def test_autocontrast_missing_required_parameters(self):
        """
        Missing any of the required autocontrast fields should return 400.
        """
        # Missing 'cutoff'
        config = {"autocontrast": {"ignore": 1, "preserve_tone": True}}
        self.post_autocontrast(config, expected_status=status.HTTP_400_BAD_REQUEST)

    def test_autocontrast_invalid_types(self):
        """
        Invalid types for parameters should return 400.
        """
        # cutoff must be numeric
        config = {"autocontrast": {"cutoff": "high", "ignore": 1, "preserve_tone": True}}
        self.post_autocontrast(config, expected_status=status.HTTP_400_BAD_REQUEST)

        # ignore must be integer
        config = {"autocontrast": {"cutoff": 10.0, "ignore": 1.5, "preserve_tone": True}}
        self.post_autocontrast(config, expected_status=status.HTTP_400_BAD_REQUEST)

        # preserve_tone must be boolean
        config = {"autocontrast": {"cutoff": 10.0, "ignore": 1, "preserve_tone": "yes"}}
        self.post_autocontrast(config, expected_status=status.HTTP_400_BAD_REQUEST)

    def test_autocontrast_out_of_range(self):
        """
        Values outside allowed ranges should return 400.
        """
        # cutoff negative
        config = {"autocontrast": {"cutoff": -1.0, "ignore": 1, "preserve_tone": True}}
        self.post_autocontrast(config, expected_status=status.HTTP_400_BAD_REQUEST)

        # ignore negative
        config = {"autocontrast": {"cutoff": 10.0, "ignore": -1, "preserve_tone": True}}
        self.post_autocontrast(config, expected_status=status.HTTP_400_BAD_REQUEST)

        # cutoff too large
        config = {"autocontrast": {"cutoff": 101.0, "ignore": 1, "preserve_tone": True}}
        self.post_autocontrast(config, expected_status=status.HTTP_400_BAD_REQUEST)

    def test_autocontrast_extra_keys(self):
        """
        Unexpected keys in autocontrast payload should not cause a server error.
        """
        config = {"autocontrast": {"cutoff": 10.0, "ignore": 1, "preserve_tone": True, "foo": "bar"}}
        # Implementation may ignore 'foo' or return 400; ensure no 500
        response = self.post_autocontrast(config)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
