import re
from datetime import date, datetime
from .exceptions import WrongNoteTextException, WrongNoteTagException, WrongRecordAddressException, WrongRecordBirthdayFormatException, WrongRecordBirthdayInFutureException ,WrongRecordEmailException, WrongRecordNameException, WrongRecordPhoneException


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value
    
    def validate(self, value):
        return True
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        if self.validate(new_value):
            self._value = new_value
        
    def __str__(self):
        return str(self.value)

#----------------------  Note fields    ----------------------#
    
class NoteID(Field):
    pass


class NoteText(Field):
    def validate(self, value:str):
        if isinstance(value, str) and len(value) >= 3:
            return True
        else:
            print(WrongNoteTextException(value))


class NoteTags(Field):
    def validate(self, value:str):
        if isinstance(value, str) and len(value) >= 3:
            return True
        else:
            print(WrongNoteTagException(value))
   
#----------------------  Record fields    ----------------------#

class Name(Field):
    def validate(self, value:str):
        if isinstance(value, str) and len(value) >= 3:
            return True
        else:
            print(WrongRecordNameException(value))    


class Phone(Field):    
    @Field.value.setter
    def value(self, new_value: str):
        if len(new_value[1:]) == 12 and new_value[1:].isdecimal() and new_value.startswith('+'):
            self._value = new_value
        elif len(new_value) == 12 and new_value.isdecimal():
            self._value = '+' + new_value
        elif len(new_value) == 10 and new_value.isdecimal():
            self._value = '+38' + new_value
        else:
            print(WrongRecordPhoneException(new_value))


class Email(Field):
    def validate(self, value:str):
        if bool(re.search(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value)):
            return True   
        else:
            print(WrongRecordEmailException(value))     


class Birthday(Field):
    def convert_to_date(self, date_str: str):
        return datetime.strptime(str(date_str), "%d.%m.%Y").date()
    
    def validate(self, date_str):
        try:
            self.convert_to_date(date_str)
            if self.convert_to_date(date_str) < date.today():
                return True
            else:
                print(WrongRecordBirthdayInFutureException(date_str))
        except ValueError:
            print(WrongRecordBirthdayFormatException(date_str))

    def days_to_birthday(self):
        if self.value == None:
            return ''
        now = datetime.now()
        birthday = datetime.strptime(str(self.value), "%d.%m.%Y")
        this_year = birthday.replace(year=date.today().year)
        next_year = birthday.replace(year=date.today().year+1)
        if this_year > now:
            days =  f"{(this_year - now).days} days to birthday"
        else:
            days =  f"{(next_year - now).days} days to birthday"
        return days
    

class Address(Field):
    def validate(self, value:str):
        print(value)
        if isinstance(value, str) and len(value.split(',')) >= 3:
            return True
        else:
            print(WrongRecordAddressException(value))