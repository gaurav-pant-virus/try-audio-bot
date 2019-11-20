import sys

from core.logger import logger


class BaseException(Exception):

    def __init__(self, **extra):
        """
        Method for automatically logging the exception when it is raised.
        """
        log_msg = self.message
        if extra:
            log_msg += " Extra info: {0}".format(extra)
        logger.error(log_msg)
        super().__init__(extra)

    def display_error(self):
        message = "\nError Message : {0}".format(self.message)
        if len(self.args):
            message += "\nExtra_info    : {0}".format(
                "\n\t".join(str(value) for value in self.args if value),
            )
        sys.stderr.write("\n{0}\n".format(message))


class MultipleCommandDefined(BaseException):
    message = "Multiple commands with same name defined."


class CommandNotDefined(BaseException):
    message = "No such command exists."


class UnimplementedMethodException(BaseException):
    message = 'Method not implemented in child class.'
