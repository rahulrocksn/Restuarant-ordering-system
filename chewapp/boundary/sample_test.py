from django.test import TestCase
from .sample import SampleBoundary
from ..common.error import Result, Error


class MockController:
    def __init__(self):
        self.get_systime_called_times = 0

    def get_systime(self) -> Result[str]:
        self.get_systime_called_times += 1
        return "test systime", None


class TestSampleBoundary(TestCase):
    def setUp(self):
        self.mock_controller = MockController()
        self.boundary = SampleBoundary(self.mock_controller)

    def test_get_systime(self):
        response = self.boundary.systime(None)
        self.assertEqual(self.mock_controller.get_systime_called_times, 1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode("utf8"),
            "The time is: test systime",
        )
