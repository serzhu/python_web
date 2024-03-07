from abc import ABC, abstractmethod
from .book_methods import AddressBook
from .notes_methods import Notes


class Commands(ABC):
    @abstractmethod
    def make_commands(self):
        pass


class BookCommands(Commands):  
    def make_commands(self):
        commands = {}
        for func in vars(AddressBook):
            if callable(getattr(AddressBook, func)) and not func.startswith("__"):
                commands[func] = 'self.book.' + func
        return commands


class NotesCommands(Commands):  
    def make_commands(self):
        commands = {}
        for func in vars(Notes):
            if callable(getattr(Notes, func)) and not func.startswith("__"):
                commands[func] = 'self.notes.' + func
        return commands


class Currency():
    def __init__(self):
        self.commands = {"show_currency_rates" : 'show_currency_rates'}


class BotCommands():
    def __init__(self, cls):
        self.exit_commands = {"exit": getattr(cls, 'exit'), "quit": getattr(cls, 'exit'), "q": getattr(cls, 'exit')}
        self.help_commands = {"help": getattr(cls, 'help'), "?": getattr(cls, 'help')}
        self.other_commands = Currency().commands
        self.all_commands = BookCommands().make_commands() | NotesCommands().make_commands() | Currency().commands

