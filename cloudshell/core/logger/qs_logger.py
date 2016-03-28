#!/usr/bin/python
import sys
import logging
from datetime import datetime
from logging import StreamHandler
import threading

import os
import re
from cloudshell.core.logger.interprocess_logger import MultiProcessingLog
from cloudshell.core.logger.qs_config_parser import QSConfigParser
import inject
from cloudshell.shell.core.context import AutoLoadCommandContext, ResourceCommandContext, ResourceRemoteCommandContext

lock = threading.Lock()

# Logging Levels
LOG_LEVELS = {
    'INFO': logging.INFO,
    'WARN': logging.WARN,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'DEBUG': logging.DEBUG}

# default settings
DEFAULT_FORMAT = '%(asctime)s [%(levelname)s]: %(name)s %(module)s - %(funcName)-20s %(message)s'
DEFAULT_TIME_FORMAT = '%Y%m%d%H%M%S'
DEFAULT_LEVEL = 'DEBUG'
# DEFAULT_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../', 'Logs')
LOG_SECTION = 'Logging'

LOGGER_CONTAINER = {}


def get_settings():
    config = {}
    # Level
    log_level = QSConfigParser.get_setting(LOG_SECTION, 'LOG_LEVEL') or DEFAULT_LEVEL
    config['LOG_LEVEL'] = log_level

    # Log format
    log_format = QSConfigParser.get_setting(LOG_SECTION, 'LOG_FORMAT') or DEFAULT_FORMAT
    config['FORMAT'] = log_format

    # log_path
    log_path = QSConfigParser.get_setting(LOG_SECTION, 'LOG_PATH')
    config['LOG_PATH'] = log_path

    # Time format
    time_format = QSConfigParser.get_setting(LOG_SECTION, 'TIME_FORMAT') or DEFAULT_TIME_FORMAT
    config['TIME_FORMAT'] = time_format

    return config


# return accessable log path or None
def get_accessible_log_path(reservation_id='Autoload', handler='default'):
    accessible_log_path = None
    config = get_settings()

    if 'LOG_PATH' in os.environ:
        log_path = os.environ['LOG_PATH']
    elif config['LOG_PATH']:
        log_path = config['LOG_PATH']
    else:
        return None

    curent_path = os.path.dirname(__file__)

    if log_path.startswith('..'):
        log_path = os.path.join(curent_path, log_path)

    time_format = config['TIME_FORMAT'] or DEFAULT_TIME_FORMAT

    log_file_name = '{0}--{1}.log'.format(handler, datetime.now().strftime(time_format))
    # log_file_name = '{0}.log'.format(handler)
    log_path = os.path.join(log_path, reservation_id)

    log_file = os.path.join(log_path, log_file_name)
    # print(log_file)

    if os.path.isdir(log_path):
        if os.access(log_path, os.W_OK):
            accessible_log_path = log_file
    else:
        try:
            os.makedirs(log_path)
            accessible_log_path = log_file
        except:
            pass

    return accessible_log_path


def log_execution_info(logger_hdlr, exec_info):
    '''Log provided execution infomrmation into provided logger on 'INFO' level
    '''
    if not hasattr(logger_hdlr, 'info_logged'):
        logger_hdlr.info_logged = True
        logger_hdlr.info('--------------- Execution Info: ---------------------------')
        for key, val in exec_info.iteritems():
            logger_hdlr.info('{0}: {1}'.format(key.ljust(20), val))
        logger_hdlr.info('-----------------------------------------------------------\n')


def _is_instance_of(context, type_name):
    return context.__class__.__name__ == type_name


@inject.params(context='context')
def get_qs_logger(logger_name='QS', context=None):

    if _is_instance_of(context, 'AutoLoadCommandContext'):
        reservation_id = 'Autoload'
        resource_name = 'Default'
    elif _is_instance_of(context, 'ResourceCommandContext'):
        reservation_id = context.reservation.reservation_id
        resource_name = context.resource.name
    elif _is_instance_of(context, 'ResourceRemoteCommandContext'):
        reservation_id = context.remote_reservation.reservation_id
        resource_name = context.remote_endpoints[0].name
    else:
        raise Exception('get_qs_logger', 'Unsuppported command context provided {0}'.format(context))

    lock.acquire()
    try:
        if reservation_id in LOGGER_CONTAINER:
            logger = LOGGER_CONTAINER[reservation_id]
        else:
            logger = create_logger(logger_name, resource_name, reservation_id)
            LOGGER_CONTAINER[reservation_id] = logger
    finally:
        lock.release()
    return logger


def create_logger(logger_name, resource_name, reservation_id):

    resource_name = re.sub(' ', '_', resource_name)
    logger_name = '%s.%s' % (logger_name, resource_name)

    config = get_settings()

    if 'LOG_LEVEL' in os.environ:
        log_level = os.environ['LOG_LEVEL']
        os.getenv()
    elif config['LOG_LEVEL']:
        log_level = config['LOG_LEVEL']
    else:
        log_level = DEFAULT_LEVEL

    logger = logging.Logger(logger_name, log_level)
    formatter = MultiLineFormatter(config['FORMAT'])
    log_path = get_accessible_log_path(reservation_id, resource_name)

    if log_path:
        # print("Logger log path: %s" % log_path)
        hdlr = MultiProcessingLog(log_path, mode='a')
        print 'Logger File Handler is: {0}'.format(hdlr.baseFilename)
    else:
        hdlr = StreamHandler(sys.stdout)

    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    return logger


import time
from functools import wraps


def qs_time_this(func):
    '''
    Decorator that reports the execution time.
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        _logger = get_qs_logger()
        start = time.time()
        _logger.info("%s started" % func.__name__)
        result = func(*args, **kwargs)
        end = time.time()
        _logger.info("%s ended taking %s" % (func.__name__, str(end - start)))
        return result

    return wrapper


def get_log_path(logger=logging.getLogger()):
    for hdlr in logger.handlers:
        if isinstance(hdlr, logging.FileHandler):
            return hdlr.baseFilename
    return None


class MultiLineFormatter(logging.Formatter):
    """Log Formatter.

       Appends log header to each line.
       """
    MAX_SPLIT = 1

    def format(self, record):
        '''formatting for one or multi-line message

        :param record:
        :return:
        '''
        s = ''

        if record.msg == '':
            return s

        try:
            s = logging.Formatter.format(self, record)
            header, footer = s.rsplit(record.message, self.MAX_SPLIT)
            s = s.replace('\n', '\n' + header)
        except Exception, e:
            print 'logger.format: Unexpected error: ' + str(e)
            print 'record = %s<<<' % record
        return s


class Loggable(object):
    """Interface for Instances which uses Logging"""
    LOG_LEVEL = LOG_LEVELS['WARN']  # Default Level that will be reported
    LOG_INFO = LOG_LEVELS['INFO']
    LOG_WARN = LOG_LEVELS['WARN']
    LOG_ERROR = LOG_LEVELS['ERROR']
    LOG_CRITICAL = LOG_LEVELS['CRITICAL']
    LOG_FATAL = LOG_LEVELS['FATAL']
    LOG_DEBUG = LOG_LEVELS['DEBUG']

    def setup_logger(self):
        '''Setup local logger instance

        :return:
        '''
        self.logger = get_qs_logger(self.__class__.__name__)
        self.logger.setLevel(self.LOG_LEVEL)
        # Logging methods aliases
        self.logDebug = self.logger.debug
        self.logInfo = self.logger.info
        self.logWarn = self.logger.warn
        self.logError = self.logger.error
