import datetime
from typing import Any

class Event:
    _observers = []
    def register(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event, data = None):
        for observer in self._observers:
            observer(event, data)

def logger(event, data):
    print(event, data)

class FileLogger:
    def __init__(self, filename):
        self.filename = filename
    
    def __call__(self, event, data):
        with open(self.filename, "a", encoding='UTF-8') as f:
            f.write(f"{datetime.datetime.now()}: [{event}] = {data}\n")

if __name__ == "__main__":
    event = Event()
    event.register(logger)
    fl = FileLogger("log.txt")
    event.register(fl)
    event.notify("puls", 65)
    event.notify("puls", 100)
    event.notify("ups", 'smth happens')
    event.unregister(fl)
    event.notify("puls", 0)
    event.notify("puls", 0)
                 