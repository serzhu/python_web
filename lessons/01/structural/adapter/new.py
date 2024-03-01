from old import LegacySystem

class NewSystem:
    def execute_operation(self, operation, value1, value2):
        if operation == "+":
            return value1 + value2
        elif operation == "-":
            return value1 - value2
        elif operation == "*":
            return value1 * value2
        elif operation == "/":
            return value1 / value2
        else:
            raise ValueError("Invalid operation")

class AdapterSystem:
    def __init__(self, system: LegacySystem):
        self.system = system

    def execute_operation(self, operation, value1, value2):
        if operation == "+":
            return self.system.execute(value1, value2, "+")
        elif operation == "-":
            return self.system.execute(value1, value2, "-")
        elif operation == "*":
            return self.system.execute(value1, value2, "*")
        elif operation == "/":
            return self.system.execute(value1, value2, "/")
        else:
            raise ValueError("Invalid operation")

if __name__ == "__main__":
    system = AdapterSystem(LegacySystem())
    result = system.execute_operation('+',5,5)
    print(result)
    result = system.execute_operation('*',5,5)
    print(result)