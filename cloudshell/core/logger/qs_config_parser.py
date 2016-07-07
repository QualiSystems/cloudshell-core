#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser
import os

DEFAULT_CONFIG_PATH = 'qs_config.ini'


class QSConfigParser:
    _configDict = None

    def __init__(self):
        self._config_parser = ConfigParser.RawConfigParser()

        file_path = os.path.dirname(__file__)

        self._config_file = os.getenv('QS_CONFIG', os.path.join(file_path, DEFAULT_CONFIG_PATH))
        self._read_config_file()
        self._create_dict()

    def _read_config_file(self):
        try:
            # print('Reading config', self._config_file)
            self._config_parser.read(self._config_file)
        except:
            pass

    def _create_dict(self):
        config_dict = {}
        for section in self._config_parser.sections():
            config_dict[section] = {}
            for key, val in self._config_parser.items(section):
                config_dict[section][key] = val.replace("'", "")
        QSConfigParser._configDict = config_dict

    @staticmethod
    def get_dict(dict_section=None):
        if QSConfigParser._configDict is None:
            QSConfigParser()
        if dict_section:
            if dict_section in QSConfigParser._configDict:
                return QSConfigParser._configDict[dict_section]
            else:
                return None
        return QSConfigParser._configDict

    @staticmethod
    def get_setting(dict_section=None, dict_key=None):
        settings_dict = QSConfigParser.get_dict(dict_section)
        if settings_dict and dict_key and dict_key.lower() in settings_dict:
            return settings_dict[dict_key.lower()]
        return None
