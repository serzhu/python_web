class LegacySystem:
    def execute(self, value1, value2, operation):
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
        
if __name__ == "__main__":
    legacy = LegacySystem()
    result = legacy.execute(5,5,'+')
    print(result)
    result = legacy.execute(5,5,'*')
    print(result)