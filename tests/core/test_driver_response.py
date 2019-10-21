from unittest import TestCase

from cloudshell.core.driver_response import DriverResponse


class TestDriverResponse(TestCase):
    def test_driver_request(self):
        inst = DriverResponse()
        self.assertEqual([], inst.actionResults)
