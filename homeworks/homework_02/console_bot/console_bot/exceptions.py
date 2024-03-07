class WrongNoteTextException(Exception):
    def __init__(self, value, message="NOTE should be string with at least 3 symbols"):
        self.value = value
        self.message = message
        super().__init__(self.message)


class WrongNoteTagException(Exception):
    def __init__(self, value, message="TAG should be string with at least 3 symbols"):
        self.value = value
        self.message = message
        super().__init__(self.message)


class WrongRecordNameException(Exception):
    def __init__(self, value, message="NAME should be string with at least 3 symbols"):
        self.value = value
        self.message = message
        super().__init__(self.message)


class WrongRecordPhoneException(Exception):
    def __init__(self, value, message="PHONE should be string with at least 10 numeric symbols"):
        self.value = value
        self.message = message
        super().__init__(self.message)


class WrongRecordEmailException(Exception):
    def __init__(self, value, message="EMAIL should have a valid email address"):
        self.value = value
        self.message = message
        super().__init__(self.message)


class WrongRecordBirthdayInFutureException(Exception):
    def __init__(self, value, message="BIRTHDAY cannot be in future"):
        self.value = value
        self.message = message
        super().__init__(self.message)

class WrongRecordBirthdayFormatException(Exception):
    def __init__(self, value, message="BIRTHDAY  format must be DD.MM.YYYY"):
        self.value = value
        self.message = message
        super().__init__(self.message)

class WrongRecordAddressException(Exception):
    def __init__(self, value, message="ADDRESS should have Country, City, Street and number"):
        self.value = value
        self.message = message
        super().__init__(self.message)
