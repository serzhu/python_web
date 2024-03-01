from abc import ABC, abstractmethod
from format import colors, wrap, splitted_text, HEADER_BOOK, SEPARATOR


class OutputInfo(ABC):
    @abstractmethod
    def make_output(self):
        pass


class BookOutputInfo(OutputInfo):
    def make_output(self, record):
        colored_name = colors.RED + str(record.name.value) + colors.END
        phones = ('; '.join(phone_obj.value for phone_obj in record.phones if phone_obj.value != None) if len(record.phones)  else '')
        email = (record.email.value if record.email and record.email.value != None  else '')
        address = (record.address.value if record.address and record.address.value != None else '')
        birthday = (colors.GREEN + record.days_to_birthday() + colors.END if record.birthday and record.birthday.value != None else '')

        return f'{colored_name:23}| {phones:30}| {email:30}| {address:30}| {birthday:10}' + SEPARATOR
    

class NotesOutputInfo(OutputInfo):
    def make_output(self, note):
        txt = wrap(note.note_text.value,98)
        list = splitted_text(txt)
        colored_id = [colors.RED + str(note.note_id.value) + colors.END]
        colored_tags = ', '.join(colors.GREEN + t.value + colors.END for t in note.tags)
        return f'{colored_id[0]:^14}| {txt[0]:100}| {colored_tags:>30}' + ''.join(list[1:]) + SEPARATOR
    
class NotesFindOutputInfo(OutputInfo):
    def make_output(self, obj, text):
        for note in obj.data.values():
            tag_obj = note.find_in_tag(text)
            text_obj = note.find_in_text(text)
            if tag_obj:
                txt = wrap(note.note_text.value,98)
                list = splitted_text(txt)
                t = tag_obj.partition(text)
                colored_tag = t[0] + colors.RED + t[1] + colors.END + t[2]
                return '{0:^5}| {1:100}| {2:30}'.format(note.note_id.value, txt[0], colored_tag) + ''.join(list[1:]) + SEPARATOR
            elif text_obj:
                txt = wrap(note.note_text.value,98)
                colored_note = []
                for item in txt:
                    n =  item.partition(text)
                    colored_note.append(n[0] + colors.RED + n[1] + colors.END + n[2])
                list = splitted_text(colored_note)               
                return '{0:^5}| {1:109}| {2:30}'.format(note.note_id.value, colored_note[0], ', '.join(t.value for t in note.tags)) + \
                      ''.join(list[1:]) + SEPARATOR