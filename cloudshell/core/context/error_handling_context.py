import traceback

from cloudshell.core.context.context_service import ContextBasedService


class ErrorHandlingContext(ContextBasedService):
    def __init__(self, context, logger):
        """
        Initializes an instance of ErrorHandlingContext
        Allows proper logging on exception
        :param context: ResourceCommandContext
        :param logger: Logger
        :type logger: Logger
        """
        self.context = context
        self.logger = logger

    def get_objects(self):
        """
        Returns context instance. Should not be called explicitly
        :return:  ErrorHandlingContext
        :rtype ErrorHandlingContext
        """
        return self

    def context_started(self):
        """
        Called upon block start. Should not be called explicitly
        :return:  ErrorHandlingContext
        :rtype ErrorHandlingContext
        """
        return self

    def context_ended(self, exc_type, exc_value, exc_traceback):
        """
        Called upon block end. Should not be called explicitly
        In case of exception during the block execution logs the error with debug severity
        and allows the same exception to be thrown
        :return:  ErrorHandlingContext
        :rtype ErrorHandlingContext
        """
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        self.logger.error('Error occurred: ' + ''.join(lines))
        return False
