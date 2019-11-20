"""
.. module:: manage.py
   :synopsis:  This script will be used to do all management tasks.
   It will run other scripts which we refer here as command. We will look for command in "commands"
   package. A typical use of this script will look like below.

   python manage.py [COMMAND] [OPTIONS] [help]
"""
import os
import sys
import time
import inspect
import traceback
import pkgutil
from collections import defaultdict
from importlib import import_module
from dotenv import load_dotenv
from core import exceptions as core_exceptions
from core import utils as core_utils
from core.logger import logger

from core.commands import BaseCommand

help_subcommands = ["help", '-h']


class ManagementUtility(object):
    """
    Encapsulates the logic of the manage.py utilities.
    """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])

    def main_help_text(self):
        """
        Returns the script's main help text, as a string.
        Return different commands grouped by modules.
        """
        usage = [
            "",
            "Type '%s help <subcommand>' for help on a specific subcommand." % self.prog_name,
            "",
            "Available subcommands:",
            "",
        ]
        commands = self.get_all_commands()
        usage.extend(sorted(commands))
        help_text = '\n'.join(usage)
        return help_text+"\n\n"

    @staticmethod
    def find_commands(base_dir):
        all_commands = []
        for loader, module_name, is_pkg in pkgutil.iter_modules([base_dir]):
            module = loader.find_module(module_name).load_module(module_name)
            commands = inspect.getmembers(
                module,
                predicate=lambda x: inspect.isclass(x) and (
                    x != BaseCommand and issubclass(x, BaseCommand)
                )
            )
            all_commands.extend(commands)
        return all_commands

    def get_all_commands(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        for package in pkgutil.walk_packages([base_dir]):
            if not package.ispkg:
                continue
            command_dir = os.path.join(base_dir, package.name, 'commands')
            all_commands = self.find_commands(command_dir)

            if not all_commands:
                continue

            for _, cmd_cls in all_commands:
                yield cmd_cls.cmd_name

    def execute(self):
        """
        Given the command-line arguments, this figures out which subcommand is
        being run, creates a parser appropriate to that command, and runs it.
        """
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = help_subcommands[0]  # Display help if no arguments were given.

        options = self.argv[2:]
        if subcommand in help_subcommands:
            if len(options) < 1:
                sys.stdout.write(self.main_help_text() + '\n')
            else:
                command_class = self.find_command_class(options[0])
                command_class.print_help(self.prog_name, options)
        else:
            self.execute_command(subcommand)

    def _find_command_class(self, base_dir, cmd_name):
        modules_list = []

        for (module_loader, module_name, ispkg) in pkgutil.walk_packages(base_dir):
            if ispkg:
                continue

            module = import_module(module_name)

        # get all sub-classes of BaseCommand
        all_commands = BaseCommand.__subclasses__()
        return all_commands

    def find_command_class(self, command_name):
        """
            Method to find the command module.
        """
        command = self._find_command_class(
            base_dir=[os.path.dirname(os.path.abspath(__file__))],
            cmd_name = command_name
        )

        # Raise exception if multiple commands with same name found
        if len(command) > 1:
            raise core_exceptions.MultipleCommandDefined(command=command_name)

        # Raise exception if command not found
        if len(command) <= 0:
            raise core_exceptions.CommandNotDefined(command=command_name)

        return command.pop()

    def execute_command(self, command_name):
        """
        1- find command modules
        2- raise exception if no command found or multiple command found.
        3- load command module and get command class object
        4- run the command
        """
        command = self.find_command_class(command_name)
        command().execute(self.argv)


def execute_from_command_line(argv=None):
    """
    A method that runs a ManagementUtility.
    """
    # load .env file
    APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path=dotenv_path)

    start_time = time.time()
    utility = ManagementUtility(argv)

    try:
        utility.execute()
    except core_exceptions.BaseException as err:
        logger.exception(str(err))
        err.display_error()
    except Exception as err:
        logger.exception(str(err))
        print("\nError Message:")
        print("\n  {0}".format(str(err)))
        print("\nTraceback:")
        print("\n  {0}".format(str(traceback.format_exc())))

    # Show below message only when sub command is given in the arguments.
    # Do not show below messages sub command is not present or sub command is 'help'.
    if len(argv) > 1 and argv[1] not in help_subcommands:
        print("\nYou can check logs at location : {0}".format(os.getenv('LOG_FILE_PATH')))
        total_time = round((time.time() - start_time), 2)
        print("Total time taken by command    : {0} seconds\n".format(total_time))


if __name__ == "__main__":
    execute_from_command_line(sys.argv)
