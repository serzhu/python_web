import inspect
from .book_methods import AddressBook
from .notes_methods import Notes
from .output import OutputInfo
from .commands import BookCommands, NotesCommands, BotCommands
from .format import colors
from .logger import logger
from .currency_rates import show_currency_rates


class BotHelpOutput(OutputInfo):
    def make_output(self):
        result = '\nBot commands:\n{0}\nBook commands:\n{1}\nNotes commands:\n{2}\n'.format \
            (", ".join([key for key in BotCommands(Bot).exit_commands | BotCommands(Bot).help_commands | BotCommands(Bot).other_commands]), \
             ", ".join(BookCommands().make_commands()), \
             ", ".join(NotesCommands().make_commands()))

        return result


class Bot:
    def __init__(self):
        self.isRunning = None
        self.book = AddressBook().deserialize()
        self.notes = Notes().deserialize()
        self.commands = BotCommands(self).all_commands

    def help(self):
        print(BotHelpOutput().make_output())

    def exit(self):
        print("Good bye")
        self.notes.serialize()
        self.book.serialize()
        self.isRunning = False

    def answer_func(self, query:str):
        command = query.split()[0]
        params = query[len(command):].strip()
        try:
            if not params:
                respond = eval(self.commands[command])()
                logger.debug(f"respond: {respond}")
                return respond
            else:
                try:
                    args = params.split(' ')
                    respond = eval(self.commands[command])(*args)
                    logger.debug(f"respond: {respond}")
                    return respond
                except TypeError:
                    return f" Use command {colors.RED + command + colors.END} with arguments {inspect.getfullargspec(eval(self.commands[command]))[6]}"
        except KeyError:
            return "Wrong command!"

    
    def run(self):
        self.isRunning = True

        while self.isRunning:
            query = input(">>> ")
            if query == "" or query in BotCommands(self).help_commands:
                self.help()
                continue
            elif query in BotCommands(self).exit_commands:
                self.exit()
            else:
                respond = self.answer_func(query)
                if respond:
                    print(respond)
                logger.debug(f"respond: {respond}")
    






                        # {
                        # 'add_contact' : self.book.add_contact,
                        # 'delete_contact' : self.book.delete_contact,
                        # 'find_contacts' : self.book.find_contacts,
                        # 'show_all_contacts' : self.book.show_all_contacts,
                        # 'add_phone' : self.book.add_phone,
                        # 'add_email' : self.book.add_email,
                        # 'add_address' : self.book.add_address,
                        # 'add_birthday' : self.book.add_birthday,
                        # } 

                        # {
                        # 'add_note' : self.notes.add_note,
                        # 'add_note_tag' : self.notes.add_note_tag,
                        # 'edit_note': self.notes.edit_note,
                        # 'edit_note_tag' : self.notes.edit_note_tag,
                        # 'find_notes' : self.notes.find_notes,
                        # 'delete_note' : self.notes.delete_note,
                        # 'show_all_notes' : self.notes.show_all_notes,
                        # } 