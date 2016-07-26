import traceback


class ErrorHandlingContext(object):
    def __init__(self, logger):
        """
        Initializes an instance of ErrorHandlingContext
        Allows proper logging on exception
        :param logger: Logger
        :type logger: Logger
        """
        self.logger = logger

    def __enter__(self):
        """
        Called upon block start. Should not be called explicitly
        :return:  ErrorHandlingContext
        :rtype ErrorHandlingContext
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Called upon block end. Should not be called explicitly
        In case of exception during the block execution logs the error with debug severity
        and allows the same exception to be thrown
        :return: True means exception handles, otherwise false
        :rtype: bool
        """
        if not exc_value:
            return True
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        self.logger.error('Error occurred: ' + ''.join(lines))
        return False
