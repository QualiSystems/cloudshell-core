from unittest import TestCase

from mock import Mock, MagicMock

from cloudshell.core.context.error_handling_context import ErrorHandlingContext


class TestErrorHandlingContext(TestCase):

    def test_log_written_when_exception_occurs(self):
        # Arrange
        logger = Mock()
        logger.error = MagicMock()
        try:

            # Act
            with ErrorHandlingContext(logger=logger):
                raise ValueError('some value error occurred')
        except ValueError:

            # Assert
            logger.error.assert_called()

    def test_log_not_written_when_exception_not_thrown(self):
        # Arrange
        logger = Mock()
        logger.error = MagicMock()

        # Act
        with ErrorHandlingContext(logger=logger):
            print 'hello world'

        # Assert
        logger.error.assert_not_called()

