from unittest import TestCase

from cloudshell.core.driver_request import DriverRequest


class TestDriverRequest(TestCase):
    def test_driver_request(self):
        inst = DriverRequest()
        self.assertEqual([], inst.actions)
