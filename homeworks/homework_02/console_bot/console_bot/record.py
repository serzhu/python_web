from .fields import  Name, Phone, Email, Address, Birthday
from .output import BookOutputInfo


class Record:
    def __init__(self, name:str):
        self.name = Name(name)
        self.phones = []
        self._email = None
        self._address = None
        self._birthday =  None

    @property
    def email(self) -> Email:
        return self._email

    @email.setter
    def email(self, email):
        self._email = Email(email)

    @property
    def birthday(self) -> Birthday:
        return self._birthday

    @birthday.setter
    def birthday(self, birthday: Birthday):
        self._birthday = Birthday(birthday)

    @property
    def address(self) -> Address:
        return self._address

    @address.setter
    def address(self, address: Address):
        self._address = Address(address)

    def add_phone(self, phone:str):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)
        return self

    def find_phone(self, phone:str):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
    
    def remove_phone(self, phone:str):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            return f'Phone {phone} not found'
    
    def edit_phone(self, phone:str, new_phone:str):
        self.remove_phone(phone)
        self.add_phone(new_phone)  

    def days_to_birthday(self):
        if self.birthday:
            return self.birthday.days_to_birthday()
        
    def __str__(self):
        return BookOutputInfo().make_output(self)
