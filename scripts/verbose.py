import sys
from enum import Enum


class MessageType(Enum):
    """
    Enum class providing 3 values - INFO, WARNING, and ERROR
    """
    INFO = ""  # No message prefix necessary for information messages
    # Any other messages will have prefixes like "Warning - " or "ERROR - "
    WARNING = "Warning - "
    ERROR = "ERROR - "

    def __str__(self):
        return self.value

    @staticmethod
    def get_color(message_type):
        """
        Get ASCII escape code color for the given MessageType argument
        :param message_type: MessageType enum
        :return: ASCII code color
        """
        if message_type == MessageType.WARNING:
            return '\033[93m'
        elif message_type == MessageType.ERROR:
            return '\033[31m'
        else:
            return ''


class Verbose:
    @staticmethod
    def _type_error_message(var_name, expected, actual):
        """
        Get a type error message to use when raising exceptions/errors in form
        :param var_name: variable name with incorrect type
        :param expected: expected type
        :param actual: actual type
        :return: error message
        """
        return "{var_name} must be of type {expected}, not {actual}".format(var_name=var_name,
                                                                            expected=expected,
                                                                            actual=actual)

    def __init__(self, verbosity_level):
        if type(verbosity_level) is not int:
            raise TypeError(self._type_error_message("verbosity_level", int, type(verbosity_level)))

        self.level = verbosity_level

    @staticmethod
    def _print(color, prefix, message):
        """
        This function is meant to be used only by print method.
        Print the message with the given prefix in the given color.
        :param color: ASCII escape code for the color
        :param prefix: prefix that is placed before the message
        :param message: message to print
        """
        print("{color}{prefix}{message}{end_color}".format(color=color, prefix=prefix,
                                                           message=message, end_color='\033[0m'))

    def print(self, message_type, message, min_level=1, stream=sys.stdout):
        """
        Print the message of the given type if the set verbose level (from program args) is equal or higher to
        the min_level given.
        :param message_type: type of message. Must be an MessageType enum value
        :param message: message to print
        :param min_level: minimum level of verbosity for the message to be printed
        :param stream: stream where the message will be printed, stdout or stderr
        :return:
        """
        if not isinstance(message_type, MessageType):
            raise TypeError("message_type has to be of type {expected}, not {actual}"
                            .format(expected=MessageType, actual=type(message_type)))

        if type(min_level) is not int:
            raise TypeError(self._type_error_message("min_level", int, type(min_level)))

        valid_streams = [sys.stdout, sys.stderr]
        if stream not in valid_streams:
            raise ValueError("Stream {stream} is not a valid output stream. Valid streams are: {valid_streams}"
                             .format(stream=stream, valid_streams=valid_streams))

        if self.level >= min_level:
            self._print(MessageType.get_color(message_type), message_type, message)
