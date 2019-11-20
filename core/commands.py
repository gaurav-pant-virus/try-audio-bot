import argparse
import os
import re

from core import exceptions as core_exceptions


class BaseCommand(object):
    """
    The base class from which all management commands ultimately
    derive.

    Use this class if you want access to all of the mechanisms which
    parse the command-line arguments and work out what code to call in
    response;

    For any command ``manage.py`` loads the command class and calls its
    ``execute()`` method.
    """
    def create_parser(self, prog_name, subcommand, additional_args=None):
        """
        Create and return the ``ArgumentParser`` which will be used to
        parse the arguments to this command.
        """
        parser = argparse.ArgumentParser(prog=prog_name)
        self.add_arguments(parser)
        return parser

    def print_help(self, prog_name, subcommand):
        """
        Print the help message for this command, derived from
        ``self.usage()``.
        Override this base class method to show custom help message specific to command.
        """
        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        pass

    def validate_args(self, cmd_options):
        """
            Method to validate the command arguments after the default validations.
        """
        pass

    def execute(self, argv):
        """
        Entry point for command execution. manage.py will call this method of
        command class.
        Lets pass all arguments, if needed used it else ignore.
        """
        parser = self.create_parser(argv[0], argv[1], argv[2:])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        self.validate_args(cmd_options)
        # Move positional args out of options to mimic legacy optparse
        args = cmd_options.pop('args', ())
        self.handle(*args, **cmd_options)

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise core_exceptions.UnimplementedMethodException(method_name="handle")
