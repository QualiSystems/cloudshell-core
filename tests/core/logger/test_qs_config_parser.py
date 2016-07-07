#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests for cloudshell.core.logger.qs_config_parser
"""

from unittest import TestCase
from cloudshell.core.logger.qs_config_parser import QSConfigParser


class TestQSConfigParser(TestCase):
    exp_response = {'Logging':
                    {'time_format': '%d-%b-%Y--%H-%M-%S',
                     'log_path': '../../Logs',
                     'log_format': '%(asctime)s [%(levelname)s]: %(name)s %(module)s - %(funcName)-20s %(message)s',
                     'log_level': 'DEBUG'}}

    def setUp(self):
        """ Recreate parser before each suite """
        self.parser = QSConfigParser()

    def test_01_get_dict(self):
        """ Test suite for get_dict method """
        self.assertEqual(self.parser.get_dict(), self.exp_response)
        QSConfigParser._configDict = None
        self.assertEqual(self.parser.get_dict(), self.exp_response)
        self.assertEqual(self.parser.get_dict("Logging"), self.exp_response["Logging"])
        self.assertIsNone(self.parser.get_dict("wrong_section_name"))

    def test_02_get_setting(self):
        """ Test suite for get_setting method """
        self.assertIsNone(self.parser.get_setting())
        self.assertIsNone(self.parser.get_setting(dict_section="wrong_section_name"))
        self.assertIsNone(self.parser.get_setting(dict_section="Logging", dict_key="wrong_setting_name"))
        self.assertEqual(self.parser.get_setting(dict_section="Logging", dict_key="log_level"),
                         self.exp_response["Logging"]["log_level"])
