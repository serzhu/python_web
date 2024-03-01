from dataclasses import dataclass

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
@dataclass
class Settings(metaclass = Singleton):
    db: str = "MySQL Database"
    port: int = 3306

class NewSettings(Settings):
    pass

if __name__ == "__main__":
    connect = Settings()
    connect_two = Settings()
    connect_three =  NewSettings()
    print(connect_two.port)
    connect.port = 5432
    print(connect_two.port)
    print(connect_three.port)


    