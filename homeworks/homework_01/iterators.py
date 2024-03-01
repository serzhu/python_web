from format import HEADER_BOOK, HEADER_NOTE


class Iterator:
    def __init__(self, object):
        self.__object = object

    def __iter__(self):
        data = list(self.__object.data.values())
        #print(HEADER)
        for i in range(0, len(data)):
            yield data[i]

class PaginatedIterator:
    def __init__(self, object, page_count: int = 1):
        self.__page_count = page_count
        self.__object = object

    @property
    def page_count(self):
        return self.__page_count

    @page_count.setter
    def page_count(self, page_count):
        if page_count < 1:
            raise ValueError("Page count have to be greater than 0")
        self.__page_count = page_count

    def __iter__(self):
        data = list(self.__object.data.values())
        page_number = 1
        for i in range(0, len(data), self.__page_count):
            print(f'\nPage {page_number}:', HEADER_NOTE)
            page_number += 1
            yield data[i:i+self.__page_count]