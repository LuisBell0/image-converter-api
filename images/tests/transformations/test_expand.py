from rest_framework import status
from rest_framework.response import Response
from ..test_setup import TestSetUp

#TODO: FIX TYPE CHECKING

class TestExpand(TestSetUp):
    def test_expand_successful_values(self):
        print("running tests")
        configuration: dict = {
            "expand": {
                "border": 10,
                "fill": "#ffffff",
            }
        }
        self.post_transformation(config_dict=configuration)

        configuration: dict = {
            "expand": {
                "border": 10,
                "fill": (255,0, 0, 0),
            }
        }
        self.post_transformation(config_dict=configuration)
        my_tuple: tuple = (10,20,30,40)
        configuration: dict = {
            "expand": {
                "border": 10,
                "fill": 10,
            }
        }
        self.post_transformation(config_dict=configuration)
        
    def test_expand_extra_keys_do_not_crash(self) -> None:
        configuration: dict = {
            "expand": {
                "border": 10,
                "fill": 10,
                "foo": "bar"
            }
        }
        self.post_transformation(config_dict=configuration)

    def test_expand_missing_required_parameters(self) -> None:
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

    def test_expand_unsuccessful_with_invalid_types(self):
        configuration: dict = {
            "expand": {
                "border": "true"
            }
        }
        response: Response = self.post_transformation(config_dict=configuration, expected_status=status.HTTP_400_BAD_REQUEST)
        detail_message: str = response.data.get("detail", "")
        self.assertIn("must be of type", detail_message)
