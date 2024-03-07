import pickle
from collections import UserDict
from pathlib import Path
from .record import Record
from .iterators import Iterator
from .format import HEADER_BOOK


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        p = Path(__file__)
        self.filename = p.parent / 'Data' / 'book.pkl'
        #self.filename = "Data\\book.pkl"

    def serialize(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def deserialize(self):
        try:
            with open(self.filename, "rb") as file:
                book = pickle.load(file)
            return book
        except FileNotFoundError:
            return self

    def add_contact(self, name:str, phone:str=None, email:str=None, birthday:str=None):
        if self.data.get(name):
            return f'Name {name} already in Contacts'
        else:
            record = Record(name)
            if phone:
                record.add_phone(phone)
            if email:
                record.email = email
            if birthday:
                record.birthday = birthday
            self.data[record.name.value] = record
            self.serialize()
          
    def delete_contact(self, name:str):
        if self.find(name):
            del self.data[name]

    def add_phone(self, name, phone:str):
        record = self.find(name)
        if record:
            record.add_phone(phone)
    
    def add_email(self, name, email:str):
        record = self.find(name)
        if record:
            if record.email and record.email.value != None:
                return f'{name}  already has email {record.email.value}'
            record.email = email
        
    def add_address(self, name:str, address:str):
        record = self.find(name)
        if record:
            if record.address and record.address.value != None:
                return f'{name}  already has address {record.address.value}'
            record.address = address

    def add_birthday(self, name, birthday:str):
        record = self.find(name)
        if record:
            if record.birthday and record.birthday.value != None:
                return f'{name}  already has birthday {record.birthday.value}'
            record.birthday = birthday
    
    def show_all_contacts(self):
        print(HEADER_BOOK)
        for item in Iterator(self):
            print(item)
    
    def find(self, name) -> Record:
        if self.data.get(name):
            record = self.data.get(name)
            return record
        print(f'Name {name} not in Book')
    
    def find_contacts(self, text:str):
        print(HEADER_BOOK)
        for item in Iterator(self):
            try:
                if text in item.name.value:
                    print(item)
                elif text in '; '.join(phone_obj.value for phone_obj in item.phones):
                    print(item)
                elif text in item.email.value:
                    print(item)
                elif text in item.address.value:
                    print(item)
            except AttributeError:
                pass
                #t = record.name.value.partition(text)
                #colored = t[0] + colors.RED + t[1] + colors.END + t[2]
