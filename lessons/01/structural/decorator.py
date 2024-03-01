class Greetings:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f'Hell {self.name}'

class GreetingDecorator:
    def __init__(self, wrapper: Greetings):
        self.wrapper = wrapper

    def greet(self):
        base_greet = self.wrapper.greet()
        return base_greet.upper()

if __name__ == '__main__':
    message = GreetingDecorator(Greetings('Alexander'))
    print(message.greet())