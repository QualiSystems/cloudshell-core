from unittest import TestCase

from cloudshell.core.driver_response_root import DriverResponseRoot


class TestDriverResponseRoot(TestCase):
    def test_driver_response_root(self):
        inst = DriverResponseRoot()
        self.assertIsNone(inst.driverResponse)
