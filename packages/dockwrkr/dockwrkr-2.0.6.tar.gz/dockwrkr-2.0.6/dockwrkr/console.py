

import sys
import os
import re
import logging
import pkgutil
import importlib
import traceback
from collections import OrderedDict
from importlib import import_module
import optparse
from getpass import getpass
from dockwrkr.exceptions import InvalidCommandError

logger = logging.getLogger(__name__)


class Parser(optparse.OptionParser):
    pass

    def format_epilog(self, formatter):
        return "\n" + self.epilog if self.epilog else ""


class PassThroughParser(Parser):
    def _process_long_opt(self, rargs, values):
        try:
            optparse.OptionParser._process_long_opt(self, rargs, values)
        except optparse.BadOptionError as err:
            self.largs.append(err.opt_str)

    def _process_short_opts(self, rargs, values):
        try:
            optparse.OptionParser._process_short_opts(self, rargs, values)
        except optparse.BadOptionError as err:
            self.largs.append(err.opt_str)


class CLI(object):
    core = None

    def __init__(self, assumeYes=False):
        self.assumeYes = assumeYes
        self.args = None
        self.options = None
        self.input = None
        self.parser = None
        self.name = None
        self.parent = None
        self.autoInitCore = True

    def getHelp(self):
        """Returns the help description for this particular command"""
        return self.getParser().format_help()

    def getHelpTitle(self):
        return ""

    def getHelpDetails(self):
        return ""

    def getUsage(self):
        return "command: USAGE [options]"

    def getParserClass(self):
        return Parser

    def getParser(self, interspersed=True):
        usage = self.getUsage()
        parserClass = self.getParserClass()
        parser = parserClass(usage=usage, conflict_handler="resolve", add_help_option=False,
                             description=self.getHelpTitle(), epilog=self.getHelpDetails())
        self.getShellOptions(parser)
        if interspersed:
            parser.enable_interspersed_args()
        else:
            parser.disable_interspersed_args()
        return parser

    def parseShellInput(self, interspersed=True):
        """Return the options and arguments for this command as a tuple"""
        parser = self.getParser(interspersed)
        (opts, args) = parser.parse_args(self.input)
        return (opts, args)

    def getShellOptions(self, optparser):
        return optparser

    def execute(self, args=None):
        self.input = args
        (self.options, self.args) = self.parseShellInput()
        return self.main()

    def initialize(self):
        pass

    def main(self):
        pass

    def getOptions(self):
        return self.options

    def hasOption(self, key):
        if self.options and hasattr(self.options, key):
            return True

    def getOption(self, key):
        if self.hasOption(key):
            return getattr(self.options, key, None)
        return None

    def getArgs(self):
        return self.args

    def hasArg(self, argno):
        if len(self.args) < argno + 1:
            return False
        return True

    def getArg(self, argno):
        if self.hasArg(argno):
            return self.args[argno]
        return None

    def read(self, msg=""):
        return input(msg)

    def readln(self, msg=""):
        return input(msg + "\n")

    def readpwd(self, msg=""):
        return getpass(msg)

    def readpwdln(self, msg=""):
        return getpass(msg + "\n")

    def ask(self, msg):
        if self.assumeYes:
            return True
        print(msg)
        res = input('Proceed? [N/y] ')
        if not res.lower().startswith('y'):
            return False
        print('... proceeding')
        return True

    def exitOK(self, msg=None):
        if msg:
            logger.info(msg)
        sys.exit(0)

    def exitHelp(self, msg=None, code=1):
        logger.info(self.getHelp())
        logger.info("")
        if msg:
            logger.info(msg)
        sys.exit(1)

    def exitError(self, msg=None, code=1):
        if msg and isinstance(msg, Exception):
            logger.error("%s (%s)" % (msg, type(msg).__name__))
        elif msg:
            logger.error(msg)
        sys.exit(1)


class Program(CLI):
    def __init__(self):
        super(Program, self).__init__()
        self.cmdString = None
        self.commandInput = None
        self.command = None
        self.core = None
        self.commands = OrderedDict()

    def setupCommands(self):
        pass

    def getCommands(self):
        k = list(self.commands.keys())
        v = [self.getCommand(x) for x in k]
        return OrderedDict(list(zip(k, v)))

    def getCommand(self, commandName):
        if commandName not in self.commands:
            raise InvalidCommandError(
                "Invalid command '%s' specified" % commandName)

        commandModule = self.commands[commandName]
        module_ = importlib.import_module(commandModule)
        class_ = getattr(module_, commandName.title())
        command = class_()
        command.parent = self
        command.name = commandName
        return command

    def addCommand(self, commandName, commandModule):
        if commandName in self.commands:
            raise ValueError(
                "Command '%s' is already registered." % commandName)
        self.commands[commandName] = commandModule

    def initCommand(self, command):
        return command

    def removeCommand(self, commandName):
        if commandName not in self.commands:
            raise ValueError("Command '%s' is not registered." % commandName)
        self.commands.pop(commandName, None)

    def getHelpDetails(self):
        helpUsage = "Commands:\n\n"
        for name, command in self.getCommands().items():
            helpUsage += "  %-20s%s\n" % (name, command.getHelpTitle())
        return helpUsage

    def setupEnv(self):
        """Setup the Environment """

    def setupLogging(self):
        if self.getOption('debug'):
            logging.getLogger('dockwrkr').handlers[0].setLevel(logging.DEBUG)

    def execute(self, args=None):
        self.input = args
        (self.options, self.args) = self.parseShellInput(False)
        self.main()

    def initialize(self):
        self.setupLogging()
        self.setupEnv()
        self.setupCommands()

    def main(self):
        try:
            self.initialize()

            if not len(self.args) > 0:
                self.exitError(
                    "Please provide a command.\n\nUse 'help' for available commands.")

            self.cmdString = self.args[0]
            self.commandInput = self.args[1:]

            if self.cmdString not in self.commands:
                return self.exitError(
                    "Invalid command '%s' specified for '%s'.\n\nUse 'help %s' for available commands." % (self.cmdString, self.name, self.name))

            self.runCommand(self.cmdString)
        except Exception as err:
            logger.error(traceback.format_exc())
            self.exitError("Error running command %s: %s" %
                           (self.cmdString, err), code=2)

    def runCommand(self, commandName):
        command = self.getCommand(commandName)
        self.command = self.initCommand(command)
        self.command.execute(self.commandInput)


class Command(CLI):
    def __init__(self):
        super(Command, self).__init__()


class SubProgram(Program):
    def initialize(self):
        self.setupCommands()
