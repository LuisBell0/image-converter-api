from rest_framework.response import Response
from rest_framework import status
from ..test_setup import TestSetUp


class TestPad(TestSetUp):
    def test_pad_successful_default(self):
        configuration = {
            "pad": {
                "size": (10, 10),
                "method": "Box",
                "color": "#ffffff",
                "centering": (0.7, 0.3),
            }
        }
        self.post_transformation(config_dict=configuration)

        configuration = {
            "pad": {
                "size": (10, 10),
                "color": 20,
            }
        }
        self.post_transformation(config_dict=configuration)
        
        configuration = {
            "pad": {
                "size": (10, 10),
                "color": (255, 0, 0),
            }
        }
        self.post_transformation(config_dict=configuration)

    def test_pad_extra_keys_do_not_crash(self):
        configuration = {
            "pad": {
                "size": (10, 10),
                "method": "Box",
                "color": "#ffffff",
                "centering": (0.7, 0.3),
                "key": "value"
            }
        }
        self.post_transformation(config_dict=configuration)
    
    def test_pad_missing_required_parameters(self):
        configuration = {
            "pad":{
                "method": "Box",
                "color": "#ffffff",
                "centering": (0.7, 0.3),
            }
        }
        response = self.post_transformation(config_dict=configuration, expected_status=status.HTTP_400_BAD_REQUEST)
        detail_message = response.data.get("detail", "")
        self.assertIn("missing required configuration key", detail_message)

    def test_pad_invalid_types(self):
        configuration = {
            "pad":{
                "size": True,
            }
        }
        response = self.post_transformation(config_dict=configuration, expected_status=status.HTTP_400_BAD_REQUEST)
        detail_message = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)

        configuration = {
            "pad":{
                "size": (1, 2),
                "method": True,
            }
        }
        response = self.post_transformation(config_dict=configuration, expected_status=status.HTTP_400_BAD_REQUEST)
        detail_message = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)

        configuration = {
            "pad":{
                "size": (1, 2),
                "color": True,
            }
        }
        response = self.post_transformation(config_dict=configuration, expected_status=status.HTTP_400_BAD_REQUEST)
        detail_message = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)

        configuration = {
            "pad":{
                "size": (1, 2),
                "centering": True
            }
        }
        response = self.post_transformation(config_dict=configuration, expected_status=status.HTTP_400_BAD_REQUEST)
        detail_message = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)

    def test_pad_out_of_range(self):
        configuration = {
            "pad":{
                "size": (100, 100),
                "method": "Box",
                "color": "#ffffff",
                "centering": (1.1, 1.1),
            }
        }
        response = self.post_transformation(config_dict=configuration, expected_status=status.HTTP_400_BAD_REQUEST)
        detail_message = response.data.get("detail", "")
        self.assertIn("out of range", detail_message)

    def test_pad_incorrect_size_tuple_length(self):
        configuration = {
            "pad":{
                "size": (100, 100, 100),
            }
        }
        response = self.post_transformation(config_dict=configuration, expected_status=status.HTTP_400_BAD_REQUEST)
        detail_message = response.data.get("detail", "")
        self.assertIn("must be a tuple of 2 ints", detail_message)
