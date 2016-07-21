from unittest import TestCase

from mock import Mock, MagicMock

from cloudshell.core.context.error_handling_context import ErrorHandlingContext


class TestLoggingSession(TestCase):

    def test_log_written_when_exception_occurs(self):
        context = Mock()
        logger = Mock()
        logger.error = MagicMock()
        try:
            with ErrorHandlingContext(context=context, logger=logger):
                raise ValueError('some value error occurred')
        except ValueError:
            self.assertTrue(logger.error.called)

