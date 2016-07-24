from unittest import TestCase

from mock import Mock, MagicMock

from cloudshell.core.context.error_handling_context import ErrorHandlingContext


class TestLoggingSession(TestCase):

    def test_log_written_when_exception_occurs(self):
        logger = Mock()
        logger.error = MagicMock()
        try:
            with ErrorHandlingContext(logger=logger):
                raise ValueError('some value error occurred')
        except ValueError:
            self.assertTrue(logger.error.called)

