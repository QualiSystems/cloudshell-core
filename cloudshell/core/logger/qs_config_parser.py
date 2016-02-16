import ConfigParser
import os

DEFAULT_CONFIG_PATH = 'qs_config.ini'


class QSConfigParser:
    _configDict = None

    def __init__(self):
        self._config_parser = ConfigParser.RawConfigParser()

        file_path = os.path.realpath(__file__)
        index = file_path.rfind('\\')
        if index != -1:
            file_path = file_path[:index + 1]

        self._config_file = os.getenv('QS_CONFIG', file_path + DEFAULT_CONFIG_PATH)
        self._readConfigFile()
        self._createDict()

    def _readConfigFile(self):
        try:
            # print('Reading config', self._config_file)
            self._config_parser.read(self._config_file)
        except:
            pass

    def _createDict(self):
        # if QSConfigParser._configDict is None:
        config_dict = {}
        for section in self._config_parser.sections():
            config_dict[section] = {}
            for key, val in self._config_parser.items(section):
                config_dict[section][key] = val.replace("'", "")
        QSConfigParser._configDict = config_dict

    @staticmethod
    def getDict(dict_section=None):
        if QSConfigParser._configDict is None:
            QSConfigParser()
        if dict_section:
            if dict_section in QSConfigParser._configDict.keys():
                return QSConfigParser._configDict[dict_section]
            else:
                return None
        return QSConfigParser._configDict

    @staticmethod
    def getSetting(dict_section=None, dict_key=None):
        settings_dict = QSConfigParser.getDict(dict_section)
        if settings_dict and dict_key.lower() in settings_dict.keys():
            return settings_dict[dict_key.lower()]
        return None
