from abc import ABC, abstractmethod

class Car:
    def __init__(self):
        self.parts = {}

    def add(self, key: str, value: str):
        self.parts[key] = value

    def show(self):
        print("авто склад з")
        for key, value in self.parts.items():
            print(f"{key}: {value}")

class Builder(ABC):

    @abstractmethod
    def build_wheels(self):
        pass

    @abstractmethod
    def build_doors(self):
        pass

    @abstractmethod
    def build_engine(self):
        pass

    @abstractmethod
    def get_results(self):
        pass

class GasCarBuilder(Builder):

    def __init__(self):
        self.car = Car()
  
    def build_wheels(self):
        self.car.add("wheels","4")

    def build_doors(self):
        self.car.add("doors","4")

    def build_engine(self):
        self.car.add("engine","1.6")

    def get_results(self)-> Car:
        return self.car

class ElectricCarBuilder(Builder):

    def __init__(self):
        self.car = Car()
  
    def build_wheels(self):
        self.car.add("wheels","4")

    def build_doors(self):
        self.car.add("doors","2")

    def build_engine(self):
        self.car.add("engine","200kW")

    def get_results(self)-> Car:
        return self.car
    
class Director:
    def __init__(self, builder:Builder):
        self.builder = builder

    def construct(self):
        self.builder.build_wheels()
        self.builder.build_doors()
        self.builder.build_engine()

if __name__   ==  "__main__":
    auto_build = GasCarBuilder()
    director = Director(auto_build)
    director.construct()
    auto = auto_build.get_results()
    auto.show()

    auto_build = ElectricCarBuilder()
    director = Director(auto_build)
    director.construct()
    auto = auto_build.get_results()
    auto.show()